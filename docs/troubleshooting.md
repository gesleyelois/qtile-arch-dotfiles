# Troubleshooting

## Validate Qtile

```sh
qtile check -c ~/.config/qtile/config.py
python -m py_compile ~/.config/qtile/config.py ~/.config/qtile/custom_treetab.py ~/.config/qtile/system_status.py
```

If checking the repository before installing:

```sh
qtile check -c qtile/config.py
python -m py_compile qtile/config.py qtile/custom_treetab.py qtile/system_status.py
```

## Broken `mypy` or `stubtest`

Old wrappers in `~/.local/bin` can break `qtile check`. Repair them with:

```sh
bash scripts/fix-python-tools.sh
```

This installs `mypy` in:

```text
~/.local/share/mypy-venv
```

and writes wrapper scripts to:

```text
~/.local/bin/mypy
~/.local/bin/stubtest
```

## Weather Shows `N/A`

Weather is fetched from `https://wttr.in` with location inferred from public IP.
If it shows `N/A`:

- confirm the machine has internet access;
- test `python -c 'import urllib.request; print(urllib.request.urlopen("https://wttr.in/?format=%l%20%t", timeout=5).read().decode())'`;
- wait for the next widget update or reload Qtile.

## App Icon Is Generic

The fallback icon means the app did not match `APP_RULES` in
`qtile/custom_treetab.py`.

Find the app's window class:

```sh
xprop WM_CLASS
```

Click the target window and add the value to `APP_RULES`.

## Restore Previous Qtile Config

The installer backs up an existing config as:

```text
~/.config/qtile.backup-YYYYMMDD-HHMMSS
```

To restore one backup:

```sh
rm ~/.config/qtile
mv ~/.config/qtile.backup-YYYYMMDD-HHMMSS ~/.config/qtile
```

