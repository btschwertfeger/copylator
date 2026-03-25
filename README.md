# Copylator

Simple clipboard translator using DeepL API with no third-party Python
dependencies.

## Features

- **Ctrl+[** : Translate German to English
- **Ctrl+]** : Translate English to German
- Desktop notifications with translation preview + copy to clipboard

## Setup

1. Install system dependencies:

```bash
sudo apt install xclip libnotify-bin
```

2. Set your DeepL API key:

```bash
echo 'export DEEPL_API_KEY="your-key-here"' >> ~/.zshrc
```

3. Make the script executable:

```bash
chmod +x translate_selection.py
```

4. Set up keyboard shortcuts in your desktop environment settings:
   - **Command for Ctrl+[**: `zsh -c 'source /path/to/.zshrc && /path/to/copylator/translate_selection.py --from DE --to EN'`
   - **Command for Ctrl+]**: `zsh -c 'source /path/to/.zshrc && /path/to/copylator/translate_selection.py --from EN --to DE'`

   Replace `/path/to/` with the full path to this directory (e.g., `/home/user/.local/bin/translate_selection.py`)

## Usage

1. Highlight or copy any text with your mouse
2. Press **Ctrl+[** (German -> English) or **Ctrl+]** (English -> German)
3. Press **Ctrl+V** to paste the translation

## How it works

The script reads your highlighted text (X11 PRIMARY selection), sends it to the
DeepL API via urllib, and places the translation in your clipboard (CLIPBOARD
selection) for pasting.
