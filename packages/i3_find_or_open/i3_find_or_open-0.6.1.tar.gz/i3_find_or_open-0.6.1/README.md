# i3-find-or-open
This repo provides a command-line tool: `i3-find-or-open` that can find a window by regex in your i3wm instance, and display it, or execute any command if it is not open.

It is intended to help you bind keys that will reliably show you a window, whether or not it is open already, but technically it is capable of showing you any window (which is uniquely identifiable by either title or class), or running an arbitrary command if it is not open.
## Installation
i3-find-or-open is available on [PyPI](https://pypi.org/project/i3_find_or_open/), and the best way to install it (if you don't want to break your system python installation) is to use [pipx](https://pypa.github.io/pipx/installation/) (N.B. there is an Arch package `python-pipx` to install this with). 
```
pipx install i3-find-or-open
```
Note that if you want to bind keys in i3 to this program, it will need to be installed for all users:
```
sudo PIPX_HOME=/opt/pipx PIPX_BIN_DIR=/usr/local/bin pipx install i3-find-or-open
```
*(or you could bind `$HOME/.local/bin/i3-find-or-open` if you'd rather not install it for everybody)*

If you do want to risk breaking your system python, you could just use `pip`. 

Or, you could install it in a virtual environment yourself (note that this is all `pipx` is doing, but you might rather manage these environments manually).

## Usage
Let's say I wanted to use this to bind `$mod+o` to open my Obsidian vault (called "vault"):
```
bindsym $mod+o exec --no-startup-id "i3-find-or-open '^.* - vault - Obsidian v([1-9]|\.)+$' 'obsidian'"
```
It's worth noting that the title regex you use will usually have to be quite specific when running from a command line, as the title of your terminal emulator will likely include the full command string (make use of `^`, and `$` tokens where possible).

Some other examples, taken from my i3 config:
```
bindsym $mod+t exec --no-startup-id "i3-find-or-open 'timetable\.ods — LibreOffice Calc' 'libreoffice --norestore ~/icl/timetable.ods'"
bindsym $mod+q exec --no-startup-id "i3-find-or-open 'qBittorrent' 'qbittorrent'"
```

You can also use the `-c` flag to match a window class instead of title if the title completely changes (like for the Spotify app).

```
bindsym $mod+s exec --no-startup-id "i3-find-or-open -c 'Spotify' 'spotify-launcher'"
```

Title and class information about any open window can be found with the `xprop` command.
