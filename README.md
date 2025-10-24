# 2025

## July

### Polybar

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


---

### Neovim

**Problem**: The parser of Neovim are conflict with that of nvim-treesitter plugin

**Solution**: `:TSUpdate` to install all the missing parser. And also change the lazy configuration:

```lua 
{
	"nvim-treesitter/nvim-treesitter",
         lazy = false,
  ...
}
```

## August

### Rofi

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

---

### **Systemd: Automate Daily Journal Updates**  

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

### Linux: Automount CIFS Share After OpenVPN Connection  

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

---

### Git: Modify author information

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

---

### Cursor: Bypass model region-blocking

**Context**: Cursor’s AI models are region-locked, requiring a proxy for access in unsupported regions.

**Problem/Need**:  
- While a system-wide TUN proxy works, it’s not an elegant solution.
- Attempting to use `proxychains` caused crashes (`zygote_host_impl_linux.cc` errors) and network timeouts.
- Needed a native proxy solution to avoid Electron compatibility issues.

**Solution/Approach**:
Configure Cursor’s proxy in user `settings.json` (`Ctrl + Shift + P` and choose `Preferences: Open User Settings (JSON)`):  
   ```json
    "http.proxy": "http://127.0.0.1:20171",
    "cursor.general.disableHttp2": true
   ```  

#proxy #electron #cursor #linux #debugging  

---
### Certbot: SSL Auto-renewal

**Context**: Managing HTTPS certificates for multiple domains via Certbot, previously done manually. The system lacked default renewal tasks.  

**Problem/Need**: Automate certificate renewal monthly via cron while preserving custom Nginx paths (`/usr/local/nginx/conf`), ensuring zero downtime.  

**Solution/Approach**:  
1. **Create cron job** (run as root):  
   ```bash
   sudo crontab -e
   ```  
2. **Monthly renewal** + safety checks:  
   ```bash
   # Primary: Renew on 1st monthly, quiet mode, reload Nginx
   15 3 1 * * /usr/bin/certbot renew --quiet --nginx-server-root /usr/local/nginx/conf --deploy-hook "/usr/local/nginx/sbin/nginx -s reload"

   # Fallback: Force renewal on 15th if cert expires in ≤30 days
   0 4 15 * * /usr/bin/bash -c '/usr/bin/certbot certificates | grep "VALID: 30" && /usr/bin/certbot renew --force-renewal --nginx-server-root /usr/local/nginx/conf --deploy-hook "/usr/local/nginx/sbin/nginx -s reload"'
   ```  
   Key arguments:  
   - `--nginx-server-root`: Custom Nginx config path  
   - `--deploy-hook`: Reload Nginx without downtime  

**Result**:  
- Certificates auto-renew monthly.  
- **Verification**:  
  ```bash
  sudo certbot certificates  # Check "Expiry Date"  
  sudo tail -f /var/log/letsencrypt/letsencrypt.log  # Monitor renewals
  ```  

**Resources**:  
- [Certbot Renewal Docs](https://eff-certbot.readthedocs.io/en/stable/using.html#renewing-certificates)  
- [crontab.guru](https://crontab.guru) (schedule helper)  

#ssl #nginx #automation #cron #letsencrypt

---
### Windows: Learn Windows 10 & Office Activation

**Context**: Automating system activation bypassing manual processes using a third-party script in an elevated PowerShell environment.  
**Problem/Need**: Simplify activation of Windows 10 and Office by executing remote scripts to handle productId keys and licensing workflows.  
**Solution/Approach**:  
```powershell  
# Run PowerShell as Administrator  
$irm https://get.activated.win | iex  
```  
*Note: `irm` (Invoke-RestMethod) downloads the script, and `iex` (Invoke-Expression) executes it.*  

**Resources**:  
- [Script Source](https://get.activated.win)  
- [Project Homepage](https://massgrave.dev)  

#tags #windows10 #msoffice #powershell #activation #scripting

---

### Zip File Extraction: GPK File Encoding
**Context**: Extracted a ZIP file (`【学生版本】研究生.zip`) in a Linux terminal (zsh), but file/directory names displayed as garbled Cyrillic text (`б╛╤з╔·░ц▒╛б┐...`) instead of Chinese characters.  
**Problem/Need**: Restore correct filenames when unzipping archives created in Windows (GBK encoding) on UTF-8 systems.  

**Solution/Approach**:  
1. Specify encoding during extraction:  
```bash
unzip -O GBK "【学生版本】研究生.zip"
```  
2. If already extracted, fix garbled names recursively using `convmv`:  
```bash
sudo apt install convmv  # Install tool
convmv -f GBK -t UTF-8 --notest -r *
```

**Result**: Filenames restored to correct Chinese characters. Verified via `ls` showing readable names.  

**Notes**:  
- Always wrap filenames with spaces/symbols in quotes: `"file (1).zip"`  
- `unar -e GBK` is a robust alternative for multi-encoding archives  

**Resources**:  
[Convmv documentation](https://www.j3e.de/linux/convmv/)  
[ZIP encoding issues](https://wiki.archlinux.org/title/Zip#Encoding_issues)  
#linux #encoding #filesystem #zsh

--- 

### OpenTabletDriver Autostart
**Context**: Setting up OpenTabletDriver daemon auto-launch on a systemd-based Linux system where the service failed to start automatically due to unmet display server conditions.  

**Problem/Need**: The `opentabletdriver.service` failed to start because it required `DISPLAY` or `WAYLAND_DISPLAY` environment variables that weren't available when the systemd user service initialized.  

**Solution/Approach**: Created a systemd service override to explicitly set environment variables and remove restrictive conditions:  
```bash
# Create override directory and config
mkdir -p ~/.config/systemd/user/opentabletdriver.service.d/
cat <<EOF > ~/.config/systemd/user/opentabletdriver.service.d/override.conf
[Unit]
# Remove failing condition checks
ConditionEnvironment=
[Service]
# Explicitly set default X11 display (Wayland requires 'WAYLAND_DISPLAY=wayland-0')
Environment="DISPLAY=${DISPLAY:-:0}"
EOF
# Apply changes
systemctl --user daemon-reload
systemctl --user enable --now opentabletdriver.service
```

**Result**: Service starts successfully after login (`systemctl --user status opentabletdriver.service` shows active/running). Verified tablet functionality responds immediately upon login.  

**Notes**:  
- Wayland users must replace `DISPLAY` with `WAYLAND_DISPLAY=wayland-0`  

**Resources**:  
[Original service file](file:///usr/lib/systemd/user/opentabletdriver.service)  
[Systemd environment variables](https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html#Environment)  
#linux #systemd #opentabletdriver #autostart

---

## October
### Build Python on musl

#### Docker error

**Context**: Working with python-build-standalone project on Manjaro Linux, attempting to build Python for x86_64-unknown-linux-musl target. The Docker build process was failing during package installation phase in Debian-based containers.

**Problem/Need**: 
- Docker build failing with "Unable to locate package" errors for essential build tools
- Outdated Debian Jessie snapshot repositories from March 2023 were no longer accessible
- Multiple packages (bzip2, ca-certificates, curl, gcc, make, etc.) could not be installed in Docker containers

**Solution/Approach**:

1. **Updated Debian base image and repositories**:
   
   In `cpython-unix/base.Dockerfile`:
```dockerfile
   # Changed from outdated Jessie with snapshots:
   FROM debian@sha256:32ad5050caffb2c7e969dac873bce2c370015c2256ff984b70c1c08b3a2816a0
   
   # To current Debian 11:
   FROM debian:11-slim
```
   Simplified repository configuration by removing complex snapshot URLs and using standard Debian repos.

2. **Fixed package compatibility**:
   
   In `cpython-unix/build.Dockerfile`:
```dockerfile
   # Changed incompatible package name:
   perl      # Not available in newer Debian
   perl-base # Available replacement
```
3. **Cleared Docker cache and rebuilt**:
```bash
   docker system prune -f
   ./build-linux.py --target x86_64-unknown-linux-musl
```
**Result**: 
- Python host compilation proceeds normally with all required build tools installed
- Extension modules compile successfully, confirming all dependencies are available
- Build process now progresses through Python 3.11 compilation as expected

**Notes**: 
- Debian Jessie snapshot repositories are unreliable; using current stable releases is more maintainable
- Package names may differ between Debian versions (perl vs perl-base)
- Docker build cache can persist problematic layers, requiring explicit cleanup

**Resources**: 
- [Docker proxy configuration documentation](https://docs.docker.com/network/proxy/)
- [Debian package archive documentation](https://www.debian.org/distrib/packages)
- [python-build-standalone project](https://github.com/indygreg/python-build-standalone)

#docker #debian #package-management #build-systems #proxy-troubleshooting

---

### Bluetooth Trust: Resolving Auto-Connect Failure  
**Context**: Linux Bluetooth service was active, but paired Sony WH-1000XM4 headphones wouldn't automatically connect on boot.  
**Problem/Need**: Device showed "Paired: yes" but **"Trusted: no"** in `bluetoothctl`, causing a "paired but not connected" state that required manual reconnection.  

**Solution/Approach**:  
1. Verify Bluetooth service status:  
```bash
sudo systemctl status bluetooth.service  # Confirmed service was active/running
```  
2. Use `bluetoothctl` to mark the device as trusted:  
```bash
bluetoothctl
[WH-1000XM4]> info 88:C9:E8:E9:44:90  # Checked "Trusted: no"
[WH-1000XM4]> trust 88:C9:E8:E9:44:90  # Set device to trusted
[CHG] Device 88:C9:E8:E9:44:90 Trusted: yes  # Success confirmation
```  
3. Restart the Bluetooth service to apply changes:  
```bash
sudo systemctl restart bluetooth  # Required after trust modification
```

**Result**: Device now shows **`Trusted: yes`** in `bluetoothctl` info output. Verified by rebooting and confirming automatic connection (no manual `connect` command needed).  

**Notes**:  
- `trust` is mandatory for auto-connect even if paired; Linux won't automatically connect without this flag.  
- `systemctl restart bluetooth` is required after trust-state changes.  
- TODOs: Monitor `/var/log/syslog` if authentication errors persist.  

**Resources**:  
- `man bluetoothd`: [bluetoothd(8) docs](https://manpages.debian.org/bluetoothd)  

#linux #bluetooth #bluetoothctl #auto-connect

---
