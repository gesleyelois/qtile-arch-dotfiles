#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

sudo install -Dm644 "$repo_dir/system/etc/vconsole.conf" /etc/vconsole.conf
sudo install -Dm644 "$repo_dir/system/etc/X11/xorg.conf.d/00-keyboard.conf" /etc/X11/xorg.conf.d/00-keyboard.conf
sudo install -Dm644 "$repo_dir/system/etc/X11/xorg.conf.d/30-touchpad.conf" /etc/X11/xorg.conf.d/30-touchpad.conf

echo "Installed keyboard and touchpad customizations. Restart Xorg/Qtile or reboot to apply all changes."

