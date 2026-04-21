# Contributing

Thanks for considering a contribution.

This repository is primarily a working desktop configuration, but contributions
are welcome when they make the setup clearer, safer, more portable or easier to
customize.

## Good Contribution Areas

- Documentation improvements.
- Bug fixes for Qtile config loading or runtime behavior.
- Safer install scripts.
- New app icon mappings for `AppIconTreeTab`.
- Small, optional customizations that are easy to disable or adapt.

## Before Opening a Pull Request

Recommended workflow:

1. Fork the repository on GitHub.
2. Clone your fork and create a feature branch.

```sh
git clone git@github.com:<your-user>/qtile-arch-dotfiles.git
cd qtile-arch-dotfiles
git checkout -b feature/short-description
```

Run:

```sh
python -m py_compile qtile/config.py qtile/custom_treetab.py qtile/system_status.py
qtile check -c qtile/config.py
```

If `qtile check` fails because `mypy` or `stubtest` wrappers are broken, run:

```sh
bash scripts/fix-python-tools.sh
```

## Style Guidelines

- Keep scripts POSIX shell or Bash with `set -euo pipefail`.
- Keep machine-specific settings documented and optional.
- Do not edit files under `/usr/lib` or other package-managed paths.
- Prefer local Qtile extensions in `qtile/` over monkey-patching installed
  packages.
- Document any new package dependency in `README.md`.

## Pull Request Checklist

- The change is documented.
- The Qtile config passes validation.
- Install scripts remain safe for existing user configs.
- The change does not assume private paths, secrets or credentials.

## Reporting Issues

When reporting a problem, include:

- Arch package versions for `qtile` and relevant tools.
- Whether you are using X11 or Wayland.
- Output from `qtile check -c ~/.config/qtile/config.py`.
- Any relevant custom changes you made after installing.
