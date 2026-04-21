#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
qtile_src="$repo_dir/qtile"
qtile_dest="$HOME/.config/qtile"
packages=(
  qtile
  lm_sensors
  ttf-nerd-fonts-symbols
  rofi
  picom
  feh
  flameshot
  brightnessctl
  libpulse
)

if command -v pacman >/dev/null 2>&1; then
  missing_packages=()
  for package in "${packages[@]}"; do
    if ! pacman -Q "$package" >/dev/null 2>&1; then
      missing_packages+=("$package")
    fi
  done

  if [ "${#missing_packages[@]}" -gt 0 ]; then
    echo "Installing missing Arch packages: ${missing_packages[*]}"
    sudo pacman -S --needed "${missing_packages[@]}"
  else
    echo "Arch packages already installed."
  fi
else
  echo "pacman not found; install dependencies manually." >&2
fi

mkdir -p "$HOME/.config"

if [ -e "$qtile_dest" ] || [ -L "$qtile_dest" ]; then
  current_target=""
  if [ -L "$qtile_dest" ]; then
    current_target="$(readlink -f "$qtile_dest" || true)"
  fi

  if [ "$current_target" != "$qtile_src" ]; then
    backup_path="$qtile_dest.backup-$(date +%Y%m%d-%H%M%S)"
    echo "Backing up existing Qtile config to $backup_path"
    mv "$qtile_dest" "$backup_path"
  fi
fi

ln -sfn "$qtile_src" "$qtile_dest"
chmod +x "$qtile_src/autostart.sh"

echo "Checking Qtile config..."
if command -v qtile >/dev/null 2>&1; then
  if ! PATH="/usr/bin:/bin" qtile check -c "$qtile_dest/config.py"; then
    echo "qtile check failed; running Python syntax check as a fallback..." >&2
    python -m py_compile "$qtile_dest/config.py" "$qtile_dest/custom_treetab.py" "$qtile_dest/system_status.py"
  fi
else
  python -m py_compile "$qtile_dest/config.py" "$qtile_dest/custom_treetab.py" "$qtile_dest/system_status.py"
fi

echo "Installed. Reload Qtile with: mod + control + r"
