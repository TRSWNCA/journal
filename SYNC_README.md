# Journal Sync

Simple tool to sync README.md posts to GitHub Gists. Only updates changed posts, creates new gists for new posts.

## Features

- 🔄 **Smart Sync**: Only updates posts that have changed
- 🆕 **Auto-Create**: New posts automatically get new gists
- 📊 **Progress Tracking**: Shows sync summary with counts
- 🎨 **Rich UI**: Beautiful terminal output with colors

## Usage

### Quick Start
```bash
# Sync all posts
./sync.sh

# Or directly with uv
uv run python journal_sync.py sync
```

### Workflow

1. **Edit README.md** with nvim (or any editor)
2. **Run sync**: `./sync.sh`
3. **Done!** Changed posts are updated, new posts get new gists

## How It Works

1. **Parse README.md**: Extracts all posts (sections starting with `###`)
2. **Compare**: Checks content hash against stored database
3. **Update**: Only syncs posts that have changed
4. **Create**: New posts get new gists automatically
5. **Track**: Updates local database with gist IDs and hashes

## Configuration

Config stored in `~/.config/journal_sync.json`:
```json
{
  "github_token": "your_token",
  "gist_id": "your_gist_id", 
  "gist_filename": "coding-journal.md",
  "default_gist_filename": "post.md"
}
```

Posts database stored in `~/.config/journal_posts.json`:
```json
{
  "posts": {
    "post-id": {
      "gist_id": "abc123",
      "content_hash": "sha256:...",
      "title": "Post Title",
      "last_modified": "2025-01-15T10:30:00Z"
    }
  }
}
```

## Installation

```bash
# Install dependencies
uv sync

# Make executable
chmod +x sync.sh
```

## Example Output

```
╭─────────────────╮
│ 🔄 Journal Sync │
╰─────────────────╯

                                  Sync Summary                                  
┏━━━━━━━━━┳━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Type    ┃ Count ┃ Posts                                                      ┃
┡━━━━━━━━━╇━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ New     │ 2     │ New Post 1, New Post 2                                     │
│ Changed │ 1     │ Updated Post                                               │
│ Total   │ 3     │                                                            │
└─────────┴───────┴────────────────────────────────────────────────────────────┘

✅ Sync completed!
📊 Processed: 2 new, 1 changed
```

## Notes

- Each post gets its own gist
- Only changed posts are updated (efficient!)
- New posts automatically create new gists
- Uses content hashing to detect changes
- Beautiful terminal output with progress indicators