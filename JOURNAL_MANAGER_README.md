# Coding Journal Manager

A TUI (Terminal User Interface) tool for managing your coding journal entries. Automatically merges entries to README.md and uploads to GitHub Gist.

## Features

- 📝 **Easy Entry Management**: Paste your generated journal entries and automatically format them
- 🔄 **Auto-Merge**: Automatically adds entries to README.md under the correct month/year section
- ☁️ **GitHub Gist Integration**: Upload your journal to GitHub Gist for sharing
- ⚙️ **Configurable**: Set up GitHub token, editor preferences, and auto-commit settings
- 🎨 **Rich TUI**: Beautiful terminal interface with colors and formatting

## Installation

1. **Install dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Make executable**:
   ```bash
   chmod +x journal_manager.py
   ```

3. **Run the installer** (optional):
   ```bash
   ./install.sh
   ```

## Usage

### First Run Setup

1. **Start the manager**:
   ```bash
   python3 journal_manager.py
   ```

2. **Configure settings**:
   - GitHub Personal Access Token (for Gist uploads)
   - Preferred text editor (vim, nano, etc.)
   - Auto-commit preferences

### Adding Journal Entries

1. **Generate your entry** using the prompt from `coding-journal-prompt.md`
2. **Run the manager**: `python3 journal_manager.py`
3. **Select option 1**: "Add new journal entry"
4. **Paste your content** when prompted
5. **Confirm** to add to README.md
6. **Choose** whether to upload to GitHub Gist

### Menu Options

- **1. Add new journal entry**: Paste and add new entries
- **2. Edit existing entry**: Open editor to modify entries
- **3. Upload to GitHub Gist**: Sync README.md to your Gist
- **4. Configuration**: Update settings
- **5. View README.md**: Preview and edit README.md
- **q. Quit**: Exit the program

## Configuration

Configuration is stored in `~/.config/journal_manager.json`:

```json
{
  "github_token": "your_github_token",
  "gist_id": "your_gist_id",
  "gist_filename": "coding-journal.md",
  "auto_commit": true,
  "editor": "vim"
}
```

### GitHub Token Setup

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with `gist` scope
3. Use the token during configuration

## File Structure

```
journal/
├── journal_manager.py          # Main TUI script
├── requirements.txt            # Python dependencies
├── install.sh                  # Installation script
├── coding-journal-prompt.md    # Prompt template
├── JOURNAL_MANAGER_README.md   # This file
└── README.md                   # Your journal (auto-updated)
```

## Workflow

1. **Generate Entry**: Use the prompt template to create your journal entry
2. **Copy Content**: Copy the generated entry
3. **Run Manager**: Execute `python3 journal_manager.py`
4. **Add Entry**: Paste content and confirm
5. **Auto-Sync**: Optionally upload to GitHub Gist

## Troubleshooting

### Missing Dependencies
```bash
pip3 install rich requests
```

### Permission Issues
```bash
chmod +x journal_manager.py
```

### GitHub Token Issues
- Ensure token has `gist` scope
- Check token hasn't expired
- Verify token is correctly saved in config

### Editor Issues
- Make sure your preferred editor is installed
- Try different editors: `vim`, `nano`, `code` (VS Code)

## Example Usage

```bash
# Start the manager
python3 journal_manager.py

# Select option 1 (Add new journal entry)
# Paste your generated journal content
# Confirm to add to README.md
# Choose to upload to GitHub Gist
```

## Tips

- Use the prompt template for consistent formatting
- Set `auto_commit: true` for automatic Gist uploads
- Keep your GitHub token secure
- Use a text editor you're comfortable with
- The manager automatically organizes entries by month/year

## License

This tool is provided as-is for personal use with your coding journal.