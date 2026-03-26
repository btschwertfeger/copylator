#!/usr/bin/env python3
# -*- mode: python; coding: utf-8 -*-
#
# Copyright (C) 2026 Benjamin Thomas Schwertfeger
# https://github.com/btschwertfeger
#
# pylint: disable=broad-exception-caught

"""
translate_selection.py
----------------------------------------------------------------
Reads the current X11 PRIMARY selection (highlighted text),
translates it via DeepL API, and writes the result to CLIPBOARD.

Usage:
    python3 translate_selection.py [--from DE] [--to EN-US]

Dependencies:
    sudo apt install xclip libnotify-bin

Config:
    export DEEPL_API_KEY="your-key-here"
    Free-tier key uses api-free.deepl.com
    Pro key uses api.deepl.com
"""

import subprocess
import sys
import os
import argparse
import urllib.request
import urllib.parse
import json

API_KEY = os.getenv("DEEPL_API_KEY", "")
NOTIFY_TIMEOUT = 3000  # ms


def notify(summary: str, body: str = "", urgency: str = "normal") -> None:
    """Send a desktop notification via notify-send.

    Args:
        summary: The notification title/summary.
        body: The notification body text (optional).
        urgency: The urgency level - "low", "normal", or "critical" (default: "normal").
    """
    try:
        subprocess.run(
            ["notify-send", "-u", urgency, "-t", str(NOTIFY_TIMEOUT), summary, body],
            check=False,
        )
    except FileNotFoundError:
        pass


def get_selection() -> str:
    """Return the current PRIMARY selection (highlighted text).

    Returns:
        The selected text, or an empty string if no text is selected or xclip fails.
    """
    try:
        result = subprocess.run(
            ["xclip", "-selection", "primary", "-out"],
            capture_output=True,
            text=True,
            timeout=3,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ""


def set_clipboard(text: str) -> None:
    """Write text to the CLIPBOARD selection (Ctrl+V buffer)."""
    with subprocess.Popen(
        ["xclip", "-selection", "clipboard"],
        stdin=subprocess.PIPE
    ) as proc:
        proc.communicate(text.encode("utf-8"))


def translate_text(text: str, source_lang: str, target_lang: str, api_key: str) -> str:
    """Translate text using DeepL API via urllib.

    Args:
        text: The text to translate.
        source_lang: The source language code (e.g., "DE", "EN").
        target_lang: The target language code (e.g., "EN-US", "FR").
        api_key: The DeepL API key.

    Returns:
        The translated text.

    Raises:
        Exception: If the API request fails or the API key is invalid.
    """
    # Detect API endpoint based on key
    base_url = (
        "https://api-free.deepl.com"
        if api_key.endswith(":fx")
        else "https://api.deepl.com"
    )
    url = f"{base_url}/v2/translate"

    data = urllib.parse.urlencode(
        {"text": text, "source_lang": source_lang, "target_lang": target_lang}
    ).encode("utf-8")

    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Authorization", f"DeepL-Auth-Key {api_key}")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")

    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["translations"][0]["text"]
    except urllib.error.HTTPError as e:
        if e.code == 403:
            raise Exception("Invalid API key") from e
        if e.code == 456:
            raise Exception("Quota exceeded") from e
        raise Exception(f"HTTP error {e.code}: {e.reason}") from e
    except urllib.error.URLError as e:
        raise Exception("Cannot reach DeepL - check your internet") from e


def main() -> None:
    """Main entry point. Translate selected text via DeepL and copy to clipboard."""
    parser = argparse.ArgumentParser(
        description="Translate selected text to clipboard via DeepL"
    )
    parser.add_argument(
        "--from", dest="src", default="DE", help="Source language code (default: DE)"
    )
    parser.add_argument(
        "--to",
        dest="tgt",
        default="EN-US",
        help="Target language code (default: EN-US)",
    )
    args = parser.parse_args()

    if not API_KEY:
        notify("Translator [ERROR]", "DEEPL_API_KEY not set.", urgency="critical")
        sys.exit(1)

    text = get_selection()
    if not text:
        notify("Translator", "No text selected.", urgency="low")
        sys.exit(0)

    try:
        translated = translate_text(text, args.src, args.tgt, API_KEY)
    except Exception as e:
        notify("Translator [ERROR]", str(e), urgency="critical")
        sys.exit(1)

    set_clipboard(translated)
    preview = translated[:120] + ("..." if len(translated) > 120 else "")
    notify("Translated [OK]", preview)


if __name__ == "__main__":
    main()
