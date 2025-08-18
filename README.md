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

### User systemctl 

**Need**: Update journal regularly.

**Solution**: Add a user system service at `.config/systemd/user/`.

File `daily-jobs.service`:

```txt
[Unit]
Description=Daily Jobs Runner
After=network.target

[Service]
Type=oneshot
ExecStart=/home/cyc/Projects/daily-jobs/bin/run-all-jobs.sh
WorkingDirectory=/home/cyc/Projects/daily-jobs
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=timers.target
```

File `daily-jobs.timer`:

```txt
[Unit]
Description=Run Daily Jobs at 12:00 PM

[Timer]
OnCalendar=12:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

Start the service:

```bash
$ systemctl --user enable daily-jobs.service
```

Here's your structured journal entry based on the OpenVPN and CIFS mount troubleshooting:

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
