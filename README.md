# Qtile Arch Dotfiles

Personal Qtile configuration for Arch Linux with persistent desktop
customizations:

- status bar markers for disk, battery, CPU, memory, CPU temperature and
  weather;
- weather from the computer location, detected by `wttr.in` through the public
  IP address;
- TreeTab with application icons from Nerd Font symbols;
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

## Weather

The bar queries `wttr.in` without a city. This asks `wttr.in` to infer the
location from the public IP address instead of hard-coding a city.

## TreeTab Icons

`qtile/custom_treetab.py` defines `AppIconTreeTab`, a local TreeTab variant that
prefixes window titles with application icons. It does not edit Qtile files in
`/usr/lib`, so Arch package updates will not overwrite the customization.

## Validate

```sh
qtile check -c ~/.config/qtile/config.py
python -m py_compile ~/.config/qtile/config.py ~/.config/qtile/custom_treetab.py
```

If `qtile check` reports only broken `mypy` or `stubtest` commands from
`~/.local/bin`, the Python compile check is still useful for validating syntax.
