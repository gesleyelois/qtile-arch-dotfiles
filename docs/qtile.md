# Qtile Desktop

## Bar

The bottom bar contains:

- current layout icon;
- workspace groups, showing only used groups plus the current group;
- prompt and active window title;
- systray;
- disk free space for `/`;
- battery percentage;
- CPU usage;
- memory usage;
- CPU package temperature;
- weather detected by `wttr.in` from the public IP address;
- volume;
- clock;
- shutdown icon.

The shutdown widget uses the `⏻` icon and a 3-second countdown.

## TreeTab

The first layout is `AppIconTreeTab`, a local extension of Qtile's TreeTab.

- Section: `Apps`.
- Panel background: black.
- Active app foreground: blue.
- Inactive app foreground: light text on black.
- Layout name: icon-only, so the bottom bar does not show `appicontreetab`.
- App labels: Nerd Font icon plus application name, e.g. ` Firefox`.
- App labels are left-aligned inside the TreeTab panel.
- Panel width: `150`.

The implementation lives in `qtile/custom_treetab.py` and does not patch Qtile
inside `/usr/lib`, so Arch package upgrades should not overwrite it.

## Dynamic Workspace Display

Qtile still defines groups `1` through `5` so the `Super + 1..5` shortcuts keep
working. The bar uses `widget.GroupBox(hide_unused=True)`, so unused empty
groups are hidden and the workspace list grows as groups receive windows.

## TreeTab Width

When the TreeTab layout is active:

- `Super + Alt + Left` decreases the `Apps` panel width by 10px.
- `Super + Alt + Right` increases the `Apps` panel width by 10px.

This changes the running layout immediately and persists the last width in
`~/.local/state/qtile-arch-dotfiles/treetab_state.json`. The `panel_width`
value in `qtile/config.py` is used as the first-run default.

## Keybindings

Modifier key: `mod4` / Super.

| Shortcut | Action |
| --- | --- |
| `Super + Left/Right/Down/Up` | Move focus |
| `Super + Tab` | Focus next window |
| `Super + Ctrl + h/l/j/k` | Grow focused window |
| `Super + Alt + Left/Right` | Decrease/increase TreeTab `Apps` panel width |
| `Super + n` | Normalize layout sizes |
| `Super + Shift + Enter` | Toggle split |
| `Super + Enter` | Open terminal |
| `Super + Ctrl + t` | Next layout |
| `Super + w` | Kill focused window |
| `Super + f` | Toggle fullscreen |
| `Super + t` | Toggle floating |
| `Super + Ctrl + r` | Reload Qtile config |
| `Super + Ctrl + q` | Shutdown Qtile |
| `Super + r` | Command prompt |
| `Super + Space` | Rofi app launcher |
| `Print` | Flameshot screenshot UI |
| `XF86MonBrightnessDown/Up` | Brightness down/up |
| `XF86AudioRaiseVolume/LowerVolume/Mute` | Volume controls |
| `Super + 1..5` | Switch group |
| `Super + Shift + 1..5` | Move focused window to group |

## Autostart

`qtile/autostart.sh` starts:

- `picom`;
- wallpaper from `$HOME/Pictures/nord-wave.png` when present;
- `flameshot`.

These tools are installed by `scripts/install.sh`.
