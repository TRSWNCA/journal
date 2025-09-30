#!/usr/bin/env python3
"""
Coding Journal Manager - TUI for managing journal entries
Automatically merges entries to README.md and uploads to GitHub Gist
"""

import os
import sys
import json
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import requests
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from rich.text import Text
    from rich.table import Table
    from rich.layout import Layout
    from rich.live import Live
    from rich.align import Align
except ImportError:
    print("Missing dependencies. Install with:")
    print("pip install rich requests")
    sys.exit(1)

class JournalManager:
    def __init__(self):
        self.console = Console()
        self.config_file = Path.home() / ".config" / "journal_manager.json"
        self.readme_path = Path("README.md")
        self.config = self.load_config()
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        default_config = {
            "github_token": "",
            "gist_id": "",
            "gist_filename": "coding-journal.md",
            "auto_commit": True,
            "editor": "vim"
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return {**default_config, **config}
            except (json.JSONDecodeError, IOError):
                self.console.print("[red]Error loading config, using defaults[/red]")
        
        return default_config
    
    def save_config(self):
        """Save configuration to file"""
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def setup_config(self):
        """Interactive configuration setup"""
        self.console.print(Panel.fit("🔧 Journal Manager Configuration", style="bold blue"))
        
        if not self.config["github_token"]:
            token = Prompt.ask("GitHub Personal Access Token", password=True)
            if token:
                self.config["github_token"] = token
        
        if not self.config["gist_id"]:
            gist_id = Prompt.ask("GitHub Gist ID (leave empty to create new)")
            if gist_id:
                self.config["gist_id"] = gist_id
        
        editor = Prompt.ask("Preferred editor", default=self.config["editor"])
        self.config["editor"] = editor
        
        auto_commit = Confirm.ask("Auto-commit to Gist after adding entries?", 
                                default=self.config["auto_commit"])
        self.config["auto_commit"] = auto_commit
        
        self.save_config()
        self.console.print("[green]Configuration saved![/green]")
    
    def get_current_month(self) -> str:
        """Get current month name"""
        return datetime.now().strftime("%B")
    
    def get_current_year(self) -> str:
        """Get current year"""
        return datetime.now().strftime("%Y")
    
    def parse_journal_entry(self, content: str) -> Dict[str, str]:
        """Parse journal entry content"""
        lines = content.strip().split('\n')
        entry = {}
        current_section = None
        current_content = []
        
        for line in lines:
            line = line.strip()
            if line.startswith('### '):
                if current_section:
                    entry[current_section] = '\n'.join(current_content).strip()
                current_section = 'title'
                entry['title'] = line[4:]
                current_content = []
            elif line.startswith('**Context**:'):
                if current_section:
                    entry[current_section] = '\n'.join(current_content).strip()
                current_section = 'context'
                current_content = [line]
            elif line.startswith('**Problem/Need**:'):
                if current_section:
                    entry[current_section] = '\n'.join(current_content).strip()
                current_section = 'problem'
                current_content = [line]
            elif line.startswith('**Solution/Approach**:'):
                if current_section:
                    entry[current_section] = '\n'.join(current_content).strip()
                current_section = 'solution'
                current_content = [line]
            elif line.startswith('**Result**:'):
                if current_section:
                    entry[current_section] = '\n'.join(current_content).strip()
                current_section = 'result'
                current_content = [line]
            elif line.startswith('**Notes**:'):
                if current_section:
                    entry[current_section] = '\n'.join(current_content).strip()
                current_section = 'notes'
                current_content = [line]
            elif line.startswith('**Resources**:'):
                if current_section:
                    entry[current_section] = '\n'.join(current_content).strip()
                current_section = 'resources'
                current_content = [line]
            elif line.startswith('#') and not line.startswith('###'):
                if current_section:
                    entry[current_section] = '\n'.join(current_content).strip()
                current_section = 'tags'
                entry['tags'] = line
                current_content = []
            elif line == '---':
                if current_section:
                    entry[current_section] = '\n'.join(current_content).strip()
                break
            else:
                current_content.append(line)
        
        if current_section:
            entry[current_section] = '\n'.join(current_content).strip()
        
        return entry
    
    def add_entry_to_readme(self, entry_content: str):
        """Add journal entry to README.md"""
        if not self.readme_path.exists():
            self.console.print("[red]README.md not found![/red]")
            return False
        
        # Parse the entry
        entry = self.parse_journal_entry(entry_content)
        if not entry.get('title'):
            self.console.print("[red]Invalid entry format![/red]")
            return False
        
        # Read current README
        with open(self.readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
        
        # Find current year section
        current_year = self.get_current_year()
        year_section = f"# {current_year}"
        
        if year_section not in readme_content:
            # Add year section at the beginning
            readme_content = f"{year_section}\n\n{readme_content}"
        
        # Find current month section
        current_month = self.get_current_month()
        month_section = f"## {current_month}"
        
        if month_section not in readme_content:
            # Add month section after year
            year_pos = readme_content.find(year_section)
            if year_pos != -1:
                insert_pos = year_pos + len(year_section) + 2
                readme_content = (readme_content[:insert_pos] + 
                                f"{month_section}\n\n" + 
                                readme_content[insert_pos:])
        
        # Add entry to month section
        month_pos = readme_content.find(month_section)
        if month_pos != -1:
            # Find end of month section
            next_section_pos = readme_content.find('\n## ', month_pos + 1)
            if next_section_pos == -1:
                next_section_pos = len(readme_content)
            
            # Insert entry
            insert_pos = next_section_pos
            entry_text = f"\n{entry_content}\n\n"
            readme_content = (readme_content[:insert_pos] + 
                            entry_text + 
                            readme_content[insert_pos:])
        
        # Write back to file
        with open(self.readme_path, 'w', encoding='utf-8') as f:
            f.write(readme_content)
        
        self.console.print("[green]Entry added to README.md[/green]")
        return True
    
    def upload_to_gist(self):
        """Upload README.md to GitHub Gist"""
        if not self.config["github_token"]:
            self.console.print("[red]GitHub token not configured![/red]")
            return False
        
        if not self.readme_path.exists():
            self.console.print("[red]README.md not found![/red]")
            return False
        
        # Read README content
        with open(self.readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        headers = {
            "Authorization": f"token {self.config['github_token']}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        if self.config["gist_id"]:
            # Update existing gist
            url = f"https://api.github.com/gists/{self.config['gist_id']}"
            data = {
                "files": {
                    self.config["gist_filename"]: {
                        "content": content
                    }
                }
            }
            response = requests.patch(url, headers=headers, json=data)
        else:
            # Create new gist
            url = "https://api.github.com/gists"
            data = {
                "description": "Coding Journal",
                "public": False,
                "files": {
                    self.config["gist_filename"]: {
                        "content": content
                    }
                }
            }
            response = requests.post(url, headers=headers, json=data)
        
        if response.status_code in [200, 201]:
            gist_data = response.json()
            if not self.config["gist_id"]:
                self.config["gist_id"] = gist_data["id"]
                self.save_config()
            self.console.print(f"[green]Successfully uploaded to Gist: {gist_data['html_url']}[/green]")
            return True
        else:
            self.console.print(f"[red]Failed to upload: {response.text}[/red]")
            return False
    
    def edit_entry(self, content: str = "") -> str:
        """Edit entry using external editor"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(content)
            temp_file = f.name
        
        try:
            # Use configured editor
            editor = self.config["editor"]
            subprocess.run([editor, temp_file], check=True)
            
            with open(temp_file, 'r', encoding='utf-8') as f:
                return f.read()
        finally:
            os.unlink(temp_file)
    
    def main_menu(self):
        """Main TUI menu"""
        while True:
            self.console.clear()
            
            # Create layout
            layout = Layout()
            layout.split_column(
                Layout(Panel.fit("📝 Coding Journal Manager", style="bold blue"), size=3),
                Layout(name="main"),
                Layout(Panel.fit("Press Ctrl+C to exit", style="dim"), size=3)
            )
            
            # Main content
            table = Table(show_header=False, box=None, padding=(0, 1))
            table.add_column(style="cyan", width=20)
            table.add_column(style="white")
            
            table.add_row("1.", "Add new journal entry")
            table.add_row("2.", "Edit existing entry")
            table.add_row("3.", "Upload to GitHub Gist")
            table.add_row("4.", "Configuration")
            table.add_row("5.", "View README.md")
            table.add_row("", "")
            table.add_row("q.", "Quit")
            
            layout["main"].update(Align.center(table))
            
            with Live(layout, refresh_per_second=4):
                choice = Prompt.ask("\nSelect option", choices=["1", "2", "3", "4", "5", "q"])
            
            if choice == "1":
                self.add_entry()
            elif choice == "2":
                self.edit_entry_menu()
            elif choice == "3":
                self.upload_to_gist()
                input("\nPress Enter to continue...")
            elif choice == "4":
                self.setup_config()
            elif choice == "5":
                self.view_readme()
            elif choice == "q":
                break
    
    def add_entry(self):
        """Add new journal entry"""
        self.console.print(Panel.fit("📝 Add New Journal Entry", style="bold green"))
        
        # Get entry content
        entry_content = Prompt.ask("Paste your journal entry content")
        
        if not entry_content.strip():
            self.console.print("[red]No content provided![/red]")
            input("\nPress Enter to continue...")
            return
        
        # Confirm before adding
        self.console.print("\n[bold]Preview:[/bold]")
        self.console.print(Panel(entry_content[:500] + "..." if len(entry_content) > 500 else entry_content))
        
        if Confirm.ask("Add this entry to README.md?"):
            if self.add_entry_to_readme(entry_content):
                if self.config["auto_commit"] and Confirm.ask("Upload to GitHub Gist?"):
                    self.upload_to_gist()
                self.console.print("[green]Entry added successfully![/green]")
            else:
                self.console.print("[red]Failed to add entry![/red]")
        
        input("\nPress Enter to continue...")
    
    def edit_entry_menu(self):
        """Edit existing entry menu"""
        self.console.print(Panel.fit("✏️ Edit Journal Entry", style="bold yellow"))
        
        # For now, just open editor with empty content
        # In a full implementation, you'd want to parse and edit existing entries
        content = self.edit_entry()
        
        if content.strip():
            if Confirm.ask("Add this edited entry to README.md?"):
                if self.add_entry_to_readme(content):
                    if self.config["auto_commit"] and Confirm.ask("Upload to GitHub Gist?"):
                        self.upload_to_gist()
                    self.console.print("[green]Entry added successfully![/green]")
                else:
                    self.console.print("[red]Failed to add entry![/red]")
        
        input("\nPress Enter to continue...")
    
    def view_readme(self):
        """View README.md content"""
        if not self.readme_path.exists():
            self.console.print("[red]README.md not found![/red]")
            input("\nPress Enter to continue...")
            return
        
        with open(self.readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Show first 1000 characters
        preview = content[:1000] + "..." if len(content) > 1000 else content
        self.console.print(Panel(preview, title="README.md Preview"))
        
        if Confirm.ask("Open full README.md in editor?"):
            subprocess.run([self.config["editor"], str(self.readme_path)])
        
        input("\nPress Enter to continue...")

def main():
    """Main entry point"""
    try:
        manager = JournalManager()
        
        # Check if first run
        if not manager.config["github_token"]:
            manager.console.print(Panel.fit("Welcome to Coding Journal Manager!\nLet's set up your configuration.", style="bold blue"))
            manager.setup_config()
        
        manager.main_menu()
        
    except KeyboardInterrupt:
        print("\nGoodbye!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()