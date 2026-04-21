# Arch Input Customizations

This repository tracks the machine's current Arch Linux input configuration.

## Keyboard

- Console keymap: `br-abnt2`.
- XKB layout: `br`.
- XKB model: `abnt2`.
- XKB option: `terminate:ctrl_alt_bksp`, which enables `Ctrl+Alt+Backspace` to
  terminate the X server.

Restore with:

```sh
sudo localectl set-keymap br-abnt2
sudo localectl set-x11-keymap br abnt2 "" terminate:ctrl_alt_bksp
```

## Touchpad

The tracked Xorg/libinput touchpad file enables natural scrolling.

Restore with:

```sh
sudo install -Dm644 system/etc/X11/xorg.conf.d/30-touchpad.conf /etc/X11/xorg.conf.d/30-touchpad.conf
```

