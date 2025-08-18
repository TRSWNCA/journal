## 2025

### July

#### Polybar

**Problem**: The icon is too small in the Polybar.

**Solution**: Use separate icon font for Polybar. Refer to [Nerd Fonts Icon Problem in Polybar](https://polybar.readthedocs.io/en/stable/user/fonts/nerd-fonts.html).

Install the icon-only font `Symbols Nerd Font`

```bash
$ wget https://github.com/ryanoasis/nerd-fonts/releases/download/v3.4.0/NerdFontsSymbolsOnly.zip
$ x NerdFontsSymbolsOnly.zip && cd NerdFontsSymbolsOnly
$ mv SymbolsNerdFontMono-Regular.ttf SymbolsNerdFont-Regular.ttf ~/.local/share/fonts/
$ fc-cache -fv
```

Set it in the Polybar configuration file.

```ini
# ~/.config/polybar/config.ini
font-0 = monospace;2
font-1 = "Symbols Nerd Font Mono:size=16"
```

#### Neovim

**Problem**: The parser of Neovim are conflict with that of nvim-treesitter plugin

**Solution**: `:TSUpdate` to install all the missing parser. And also change the lazy configuration:

```lua 
{
	"nvim-treesitter/nvim-treesitter",
         lazy = false,
  ...
}
```

### August

#### Rofi

**Need**: Looking up dictionary with Rofi.

**Solution**: With Rofi dmenu mode, we can easily add scripts that can be found by rofi.

Add a query scripts with [kd](https://github.com/Karmenzind/kd)

```bash
#!/bin/bash
# Get Queries
query_word=$(rofi -dmenu -p "dict")

# Execute
termite -r pop-up -e "kd $query_word"
```

And move it into one of the paths shown by:

```bash
$ G_MESSAGES_DEBUG=Modes.Run rofi -show run -no-config
```

And then try rofi

```bash
$ rofi -combi-modi run,window,drun -show combi -modi combi -dpi 1

```

Here’s your rewritten journal entry in the new structured format, with added clarity, context, and tags:

---

#### **Systemd: Automate Daily Journal Updates**  
**Context**: Needed to run a daily script to update my coding journal without manual intervention.  
**Need**: Schedule regular journal updates via a user-level systemd service (no root required).  

**Solution**: Created a systemd timer and service for my user:  
```ini
# ~/.config/systemd/user/daily-jobs.service  
[Unit]  
Description=Daily Jobs Runner  
After=network.target  

[Service]  
Type=oneshot  
ExecStart=/home/cyc/Projects/daily-jobs/bin/run-all-jobs.sh  
WorkingDirectory=/home/cyc/Projects/daily-jobs  
StandardOutput=journal  # Logs to user journal  
StandardError=journal  

[Install]  
WantedBy=timers.target  
```  
```ini
# ~/.config/systemd/user/daily-jobs.timer  
[Unit]  
Description=Run Daily Jobs at 12:00 PM  

[Timer]  
OnCalendar=12:00:00  # Triggers daily at noon  
Persistent=true      # Run if missed during downtime  

[Install]  
WantedBy=timers.target  
```  
**Activation**:  
```bash
systemctl --user enable --now daily-jobs.timer  # Start and enable  
```  

**Result**:  
- Script now runs daily at 12:00 PM (verify with `journalctl --user -u daily-jobs`).  
- Logs appear in the user journal (`--user-unit=daily-jobs`).  

**Resources**:  
- [Systemd User Services Docs](https://wiki.archlinux.org/title/Systemd/User)  

#systemd #automation #linux  
---

#### Linux: Automount CIFS Share After OpenVPN Connection  

**Need**: Automatically mount a network share (`//192.168.1.3/Team_Folder`) only after a VPN connection establishes. Systemd dependencies and credential security were key requirements.  

**Solution**:  
1. **Credential File Setup**:  
   ```bash
   sudo mkdir /etc/credentials
   sudo tee /etc/credentials/tank-cifs.cred <<EOF
   username=<name>
   password=<password>
   EOF
   sudo chmod 600 /etc/credentials/tank-cifs.cred
   ```

2. **Systemd Mount Unit**:  
   ```ini
   # /etc/systemd/system/mnt-tank.mount
   [Unit]
   Description=Mount Team_Folder
   Requires=tank-openvpn.service
   After=tank-openvpn.service network-online.target

   [Mount]
   What=//192.168.1.3/Team_Folder
   Where=/mnt/tank
   Type=cifs
   Options=vers=3.0,credentials=/etc/credentials/tank-cifs.cred,uid=1000,gid=1000
   ```

**Result**:  
- Successfully mounts after VPN establishes (`systemctl status mnt-tank.mount` shows active)  
- Verified with `mount | grep /mnt/tank` and file access tests  

**Notes**:  
- Requires `network-online.target` for reliable startup  
- `_netdev` mount option is not needed since OpenVPN startup after the network is ready

**Resources**:  
- [systemd.mount docs](https://www.freedesktop.org/software/systemd/man/systemd.mount.html)  
- [CIFS mount options](https://linux.die.net/man/8/mount.cifs)  

#linux #systemd #vpn #cifs #automount  

#### Git: Modify author information

**Context**: In a Git - based project, there were multiple commits made with an incorrect author. To ensure proper attribution, it was necessary to change the author of these commits to `Chen Yichi <trswnca@yeah.net>`.

**Problem/Need**: Change the author information of six specific commits in the Git repository to `Chen Yichi <trswnca@yeah.net>`.

**Solution/Approach**:
1. Start an interactive rebase:
```bash
git rebase -i 2028312c0e4325e5eccbc72f12fe47adbce2df98^
```
The `^` is used to include the specified commit in the rebase range.

2. Edit the rebase file:
Open the file in the text editor that appears after the above command. Change each line starting with `pick` to `edit`. For example:
```
edit 2028312c0e4325e5eccbc72f12fe47adbce2df98 fix: embedding provider for dataloader is missing
edit cd9975f7e7e7a5df7cf7b9d7c564f89cd169d993 feat: Add langchain mode and introduce python - dotenv
#... and so on for all relevant commits
```
Save and close the file.

3. Modify the author information for each commit:
When the rebase pauses at each `edit` commit, run the following command to change the author without editing the commit message:
```bash
git commit --amend --author="Chen Yichi <trswnca@yeah.net>" --no - edit
```

4. Continue the rebase:
After modifying the author of a commit, run the following command to move on to the next commit:
```bash
git rebase --continue
```

5. Force - push the changes to the remote repository:
```bash
git push -f origin master
```

**Result**: The author information of the specified six commits in the local and remote Git repository should now show as `Chen Yichi <trswnca@yeah.net>`. Verification can be done by running `git log` in the local repository and checking the author information of the relevant commits. Also, visit the remote repository on the hosting platform (e.g., GitHub) and check the commit history there.

#git #coding #author
