# Input Profile

This repository tracks an optional Arch Linux input profile. It matches the
author's current machine and is useful for Brazilian ABNT2 keyboards.

Do not install these files blindly if you use a different keyboard layout.

## Keyboard

- Console keymap: `br-abnt2`.
- XKB layout: `br`.
- XKB model: `abnt2`.
- XKB option: `terminate:ctrl_alt_bksp`, which enables `Ctrl+Alt+Backspace` to
  terminate the X server.

Apply with:

```sh
sudo localectl set-keymap br-abnt2
sudo localectl set-x11-keymap br abnt2 "" terminate:ctrl_alt_bksp
```

## Touchpad

The tracked Xorg/libinput touchpad file enables natural scrolling.

Install with:

```sh
sudo install -Dm644 system/etc/X11/xorg.conf.d/30-touchpad.conf /etc/X11/xorg.conf.d/30-touchpad.conf
```

To install all tracked input files at once:

```sh
bash scripts/install-system-input.sh
```
