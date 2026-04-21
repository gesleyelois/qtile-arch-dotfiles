# Customization Guide

Use this repository as a starting point, not as a one-size-fits-all desktop.

## Change Default Programs

Main config file:

```text
qtile/config.py
```

Common settings to change:

- `terminal = guess_terminal()` if you want a fixed terminal command.
- `lazy.spawn("rofi -show drun")` if you use a different launcher.
- `qtile/autostart.sh` if you do not use `picom`, `feh` or `flameshot`.

## Add App Icons to TreeTab

Edit:

```text
qtile/custom_treetab.py
```

Add a rule to `APP_RULES`:

```python
(("wm-class-or-title-fragment",), "ICON", "Display Name"),
```

Rules are matched against window class, role and title. Prefer stable
`wm_class` values when possible.

## Change TreeTab Width

Default width is configured in `qtile/config.py`:

```python
panel_width=150
```

At runtime, when TreeTab is active:

- `Super + Alt + Left`: decrease width by 10px.
- `Super + Alt + Right`: increase width by 10px.

Runtime changes reset after Qtile reload. Change `panel_width` to make a new
default permanent.

## Change Workspaces

Groups are defined in `qtile/config.py`:

```python
groups = [Group(i) for i in "12345"]
```

The bar uses `widget.GroupBox(hide_unused=True)`, so empty unused groups are
hidden even though they still exist for keyboard shortcuts.

## Change Keyboard Layout

The tracked input profile is ABNT2. If you do not use Brazilian ABNT2, do not
run `scripts/install-system-input.sh` as-is.

For another layout, update:

- `system/etc/vconsole.conf`
- `system/etc/X11/xorg.conf.d/00-keyboard.conf`
- `docs/input.md`

