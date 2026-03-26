# Copylator

Translate highlighted text via DeepL API to bind with a keyboard shortcut.

**Note:** X11 only (Linux with xclip support).

## Setup

1. Install dependencies:
   ```bash
   sudo apt install xclip libnotify-bin
   ```

2. Make executable:
   ```bash
   chmod +x translate_selection.py
   ```

3. Set your DeepL API key in your shell environment:
   ```zsh
   # e.g. ~/.zshrc
   export DEEPL_API_KEY="your-key-here"
   ```
   The API key must be available in the environment where the script runs.

4. Example setup: Add keyboard shortcuts in Ubuntu 24.04 Settings:
   - Open **Settings** > **Keyboard** > **View and Customize Shortcuts** > **Custom Shortcuts**
   - Add new shortcut with command:
     ```
     zsh -c 'source /path/to/.zshrc && /path/to/translate_selection.py --from DE --to EN'
     ```
     (Replace `/path/to/` with full path actually used)
   - Assign a keyboard binding (e.g., `Ctrl+[`)
   - Do the same for other translation direction using another keybinding

## Usage

1. Highlight text anywhere
2. Press your configured shortcut
3. Translation appears in clipboard and notification
4. Press `Ctrl+V` to paste
