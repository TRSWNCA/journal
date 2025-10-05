#!/usr/bin/env python3
"""
Journal Sync - Simple tool to sync README.md posts to GitHub Gists
Only updates changed posts, creates new gists for new posts
"""

import os
import sys
import json
import hashlib
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

try:
    import requests
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
except ImportError:
    print("Missing dependencies. Install with: uv add rich requests")
    sys.exit(1)

class JournalSync:
    def __init__(self):
        self.console = Console()
        self.readme_path = Path("README.md")
        self.config_file = Path.home() / ".config" / "journal_sync.json"
        self.posts_db_file = Path.home() / ".config" / "journal_posts.json"
        
        # Load configuration
        self.config = self.load_config()
        self.posts_db = self.load_posts_db()
        
    def load_config(self) -> Dict:
        """Load configuration from file"""
        default_config = {
            "github_token": "",
            "gist_id": "",
            "gist_filename": "coding-journal.md",
            "default_gist_filename": "post.md"
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return {**default_config, **config}
            except (json.JSONDecodeError, IOError):
                self.console.print("[red]Error loading config, using defaults[/red]")
        
        return default_config
    
    def load_posts_db(self) -> Dict:
        """Load posts database from file"""
        if self.posts_db_file.exists():
            try:
                with open(self.posts_db_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                self.console.print("[red]Error loading posts DB, starting fresh[/red]")
        
        return {"posts": {}}
    
    def save_posts_db(self):
        """Save posts database to file"""
        self.posts_db_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.posts_db_file, 'w') as f:
            json.dump(self.posts_db, f, indent=2)
    
    def parse_readme_posts(self) -> List[Dict]:
        """Parse README.md and extract all posts"""
        if not self.readme_path.exists():
            self.console.print("[red]README.md not found![/red]")
            return []
        
        with open(self.readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        posts = []
        lines = content.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for post headers (### Tool/Technology Name)
            if line.startswith('### ') and not line.startswith('####'):
                post_title = line[4:].strip()
                
                # Find the end of this post (next ### or end of file)
                start_line = i
                end_line = i
                
                # Look for the end of this post
                j = i + 1
                while j < len(lines):
                    if lines[j].strip().startswith('### ') and not lines[j].strip().startswith('####'):
                        end_line = j - 1
                        break
                    j += 1
                else:
                    end_line = len(lines) - 1
                
                # Extract post content
                post_content = '\n'.join(lines[start_line:end_line + 1])
                
                # Generate post ID from title
                post_id = self.generate_post_id(post_title)
                
                # Calculate content hash
                content_hash = hashlib.sha256(post_content.encode()).hexdigest()
                
                posts.append({
                    'id': post_id,
                    'title': post_title,
                    'content': post_content,
                    'content_hash': content_hash,
                    'start_line': start_line,
                    'end_line': end_line
                })
                
                i = j
            else:
                i += 1
        
        return posts
    
    def generate_post_id(self, title: str) -> str:
        """Generate a unique post ID from title"""
        # Convert title to lowercase, replace spaces with hyphens, remove special chars
        import re
        post_id = re.sub(r'[^\w\s-]', '', title.lower())
        post_id = re.sub(r'[-\s]+', '-', post_id)
        return post_id.strip('-')
    
    def get_changed_posts(self, current_posts: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
        """Compare current posts with database to find changes"""
        changed_posts = []
        new_posts = []
        
        for post in current_posts:
            post_id = post['id']
            
            if post_id in self.posts_db['posts']:
                # Existing post - check if content changed
                stored_hash = self.posts_db['posts'][post_id]['content_hash']
                if post['content_hash'] != stored_hash:
                    changed_posts.append(post)
            else:
                # New post
                new_posts.append(post)
        
        return changed_posts, new_posts
    
    def create_gist(self, post: Dict) -> Optional[str]:
        """Create a new gist for a post"""
        headers = {
            "Authorization": f"token {self.config['github_token']}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Use post title as filename
        filename = f"{post['id']}.md"
        
        data = {
            "description": f"Coding Journal: {post['title']}",
            "public": True,
            "files": {
                filename: {
                    "content": post['content']
                }
            }
        }
        
        try:
            response = requests.post("https://api.github.com/gists", 
                                   headers=headers, json=data)
            
            if response.status_code == 201:
                gist_data = response.json()
                gist_id = gist_data['id']
                self.console.print(f"[green]Created gist for '{post['title']}': {gist_data['html_url']}[/green]")
                return gist_id
            else:
                self.console.print(f"[red]Failed to create gist: {response.text}[/red]")
                return None
                
        except Exception as e:
            self.console.print(f"[red]Error creating gist: {e}[/red]")
            return None
    
    def update_gist(self, post: Dict, gist_id: str) -> bool:
        """Update an existing gist"""
        headers = {
            "Authorization": f"token {self.config['github_token']}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        # Get current gist to find filename
        try:
            response = requests.get(f"https://api.github.com/gists/{gist_id}", headers=headers)
            if response.status_code != 200:
                self.console.print(f"[red]Failed to get gist info: {response.text}[/red]")
                return False
            
            gist_data = response.json()
            files = gist_data['files']
            
            # Find the markdown file (should be only one)
            filename = None
            for file_key in files.keys():
                if file_key.endswith('.md'):
                    filename = file_key
                    break
            
            if not filename:
                self.console.print("[red]No markdown file found in gist[/red]")
                return False
            
            # Update the gist
            data = {
                "description": f"Coding Journal: {post['title']}",
                "files": {
                    filename: {
                        "content": post['content']
                    }
                }
            }
            
            response = requests.patch(f"https://api.github.com/gists/{gist_id}", 
                                    headers=headers, json=data)
            
            if response.status_code == 200:
                self.console.print(f"[green]Updated gist for '{post['title']}': {response.json()['html_url']}[/green]")
                return True
            else:
                self.console.print(f"[red]Failed to update gist: {response.text}[/red]")
                return False
                
        except Exception as e:
            self.console.print(f"[red]Error updating gist: {e}[/red]")
            return False
    
    def sync(self):
        """Main sync function"""
        self.console.print(Panel.fit("🔄 Journal Sync", style="bold blue"))
        
        # Parse current posts from README.md
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            task = progress.add_task("Parsing README.md...", total=None)
            current_posts = self.parse_readme_posts()
            progress.update(task, description=f"Found {len(current_posts)} posts")
        
        if not current_posts:
            self.console.print("[yellow]No posts found in README.md[/yellow]")
            return
        
        # Find changed and new posts
        changed_posts, new_posts = self.get_changed_posts(current_posts)
        
        # Display summary
        table = Table(title="Sync Summary")
        table.add_column("Type", style="cyan")
        table.add_column("Count", style="green")
        table.add_column("Posts", style="white")
        
        table.add_row("New", str(len(new_posts)), 
                     ", ".join([p['title'][:30] + "..." if len(p['title']) > 30 
                               else p['title'] for p in new_posts]))
        table.add_row("Changed", str(len(changed_posts)), 
                     ", ".join([p['title'][:30] + "..." if len(p['title']) > 30 
                               else p['title'] for p in changed_posts]))
        table.add_row("Total", str(len(current_posts)), "")
        
        self.console.print(table)
        
        if not new_posts and not changed_posts:
            self.console.print("[green]No changes detected. All posts are up to date![/green]")
            return
        
        # Process new posts
        for post in new_posts:
            self.console.print(f"\n[bold]Creating gist for new post: {post['title']}[/bold]")
            gist_id = self.create_gist(post)
            if gist_id:
                # Update posts database
                self.posts_db['posts'][post['id']] = {
                    'gist_id': gist_id,
                    'content_hash': post['content_hash'],
                    'title': post['title'],
                    'last_modified': datetime.now().isoformat()
                }
        
        # Process changed posts
        for post in changed_posts:
            self.console.print(f"\n[bold]Updating gist for changed post: {post['title']}[/bold]")
            stored_post = self.posts_db['posts'][post['id']]
            gist_id = stored_post['gist_id']
            
            if self.update_gist(post, gist_id):
                # Update posts database
                self.posts_db['posts'][post['id']].update({
                    'content_hash': post['content_hash'],
                    'last_modified': datetime.now().isoformat()
                })
        
        # Save updated database
        self.save_posts_db()
        
        self.console.print(f"\n[green]✅ Sync completed![/green]")
        self.console.print(f"📊 Processed: {len(new_posts)} new, {len(changed_posts)} changed")

def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "sync":
        sync = JournalSync()
        sync.sync()
    else:
        print("Usage: python journal_sync.py sync")
        print("This will sync your README.md posts to GitHub Gists")

if __name__ == "__main__":
<<<<<<< HEAD
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> ebd5295 (updated by daily-jobs.service)
=======
    main()
>>>>>>> 06ef7dd (Remove hardcoded GitHub token from default config)
