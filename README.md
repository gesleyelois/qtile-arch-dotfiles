# Qtile Arch Dotfiles

Opinionated Qtile dotfiles for Arch Linux. The goal is to keep desktop
customizations in a Git repository instead of editing files that can be lost
after package or system updates.

## What This Includes

- A Qtile config with a bottom status bar for disk, battery, CPU, memory, CPU
  temperature, weather, volume, clock and shutdown.
- A custom TreeTab layout that shows `icon + application name` instead of full
  window titles.
- Dynamic workspace display: empty unused groups are hidden from the bar.
- Keybindings for TreeTab width control, screenshots, brightness, volume,
  window management and workspace navigation.
- Optional Arch input files for ABNT2 keyboard layout and natural touchpad
  scrolling.
- Install and repair scripts for repeatable setup.

## Requirements

Supported target: Arch Linux with Qtile on X11.

Install dependencies manually:

```sh
sudo pacman -S --needed qtile lm_sensors ttf-nerd-fonts-symbols rofi picom feh flameshot brightnessctl libpulse
```

Or let the installer check and install missing packages after cloning this
repository:

```sh
bash scripts/install.sh
```

Notes:

- The config reads CPU, memory, temperature and weather through local Python
  helpers, so it does not require Qtile's optional `python-psutil` or
  `python-aiohttp` widgets.
- Weather uses `wttr.in` and infers location from public IP. No city is
  hard-coded.
- `pactl` is provided by the Arch `libpulse` package.

## Install

```sh
git clone https://github.com/gesleyelois/qtile-arch-dotfiles.git ~/Workspaces/qtile-arch-dotfiles
cd ~/Workspaces/qtile-arch-dotfiles
bash scripts/install.sh
```

The installer:

- installs missing Arch packages from the requirements list;
- backs up an existing `~/.config/qtile` directory;
- creates `~/.config/qtile -> ~/Workspaces/qtile-arch-dotfiles/qtile`;
- validates the Qtile config.

Reload Qtile after installing:

```text
Super + Ctrl + r
```

## Optional System Input Files

The repository tracks this machine's Arch input profile under `system/`:

- `system/etc/vconsole.conf`: console keymap `br-abnt2` and XKB defaults.
- `system/etc/X11/xorg.conf.d/00-keyboard.conf`: Xorg `br` layout, `abnt2`
  model and `terminate:ctrl_alt_bksp`.
- `system/etc/X11/xorg.conf.d/30-touchpad.conf`: libinput natural scrolling.

These files affect system-wide input behavior. Review them before installing:

```sh
bash scripts/install-system-input.sh
```

See [docs/input.md](docs/input.md) for details.

## Documentation

- [Qtile desktop](docs/qtile.md): widgets, TreeTab behavior, keybindings and
  autostart.
- [Input profile](docs/input.md): ABNT2 keyboard and touchpad configuration.
- [Customization guide](docs/customization.md): how to adapt this repo for your
  own machine.
- [Troubleshooting](docs/troubleshooting.md): common issues and validation
  commands.
- [Contributing](CONTRIBUTING.md): how to propose improvements.

## Validate

```sh
qtile check -c ~/.config/qtile/config.py
python -m py_compile ~/.config/qtile/config.py ~/.config/qtile/custom_treetab.py ~/.config/qtile/system_status.py
```

If old user-local Python wrappers break `qtile check`, repair them with:

```sh
bash scripts/fix-python-tools.sh
```

## Contributing

Issues and pull requests are welcome. Please keep changes portable, documented
and validated with `qtile check`. See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT. See [LICENSE](LICENSE).
