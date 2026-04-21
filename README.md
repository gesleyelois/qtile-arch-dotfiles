# Qtile Arch Dotfiles

Personal Qtile configuration for Arch Linux with persistent desktop
customizations:

- status bar markers for disk, battery, CPU, memory, CPU temperature and
  weather;
- weather from the computer location, detected by `wttr.in` through the public
  IP address;
- TreeTab with application icons from Nerd Font symbols;
- Arch input customizations for ABNT2 keymap and natural touchpad scrolling;
- install script that keeps the active Qtile config as a symlink to this repo.

## Requirements

Arch Linux packages:

```sh
sudo pacman -S --needed qtile lm_sensors ttf-nerd-fonts-symbols
```

CPU, memory, temperature and weather are read by local helper functions, so the
config does not depend on Qtile's optional `python-psutil` or `python-aiohttp`
widgets.

## Install

```sh
git clone https://github.com/gesleyelois/qtile-arch-dotfiles.git ~/Workspaces/qtile-arch-dotfiles
cd ~/Workspaces/qtile-arch-dotfiles
bash scripts/install.sh
```

The installer backs up an existing `~/.config/qtile` directory before creating
the symlink:

```text
~/.config/qtile -> ~/Workspaces/qtile-arch-dotfiles/qtile
```

Reload Qtile after installing:

```text
mod + control + r
```

## Documentation

- [Qtile desktop](docs/qtile.md): widgets, TreeTab, shutdown icon and keybindings.
- [Arch input](docs/input.md): ABNT2 keymap, XKB options and touchpad natural scrolling.
- `scripts/fix-python-tools.sh`: repairs stale `~/.local/bin/mypy` and
  `~/.local/bin/stubtest` wrappers by installing `mypy` in a dedicated venv.

## System Input Customizations

The current Arch Linux keyboard and touchpad customizations are versioned under
`system/`:

- `system/etc/vconsole.conf`: console keymap `br-abnt2` and XKB `br`/`abnt2`.
- `system/etc/X11/xorg.conf.d/00-keyboard.conf`: Xorg keyboard layout `br`,
  model `abnt2` and `terminate:ctrl_alt_bksp`.
- `system/etc/X11/xorg.conf.d/30-touchpad.conf`: libinput natural scrolling.

To restore these system files on a fresh install:

```sh
sudo install -Dm644 system/etc/vconsole.conf /etc/vconsole.conf
sudo install -Dm644 system/etc/X11/xorg.conf.d/00-keyboard.conf /etc/X11/xorg.conf.d/00-keyboard.conf
sudo install -Dm644 system/etc/X11/xorg.conf.d/30-touchpad.conf /etc/X11/xorg.conf.d/30-touchpad.conf
```

Apply keyboard settings without editing by hand:

```sh
sudo localectl set-keymap br-abnt2
sudo localectl set-x11-keymap br abnt2 "" terminate:ctrl_alt_bksp
```

## Weather

The bar queries `wttr.in` without a city. This asks `wttr.in` to infer the
location from the public IP address instead of hard-coding a city.

## TreeTab Icons

`qtile/custom_treetab.py` defines `AppIconTreeTab`, a local TreeTab variant that
prefixes window titles with application icons. It does not edit Qtile files in
`/usr/lib`, so Arch package updates will not overwrite the customization.

The TreeTab panel uses a black background and the custom layout is named with an
icon so the bottom bar does not show the text `appicontreetab`.

## Validate

```sh
PATH=/usr/bin:/bin qtile check -c ~/.config/qtile/config.py
python -m py_compile ~/.config/qtile/config.py ~/.config/qtile/custom_treetab.py
```

Using a minimal `PATH` avoids false failures from broken user-local `mypy` or
`stubtest` commands in `~/.local/bin`.

To repair those commands instead of bypassing them:

```sh
bash scripts/fix-python-tools.sh
```
