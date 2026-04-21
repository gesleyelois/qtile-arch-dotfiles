#!/bin/sh

pgrep -x picom >/dev/null 2>&1 || picom &

if [ -f "$HOME/Pictures/nord-wave.png" ]; then
    feh --bg-scale "$HOME/Pictures/nord-wave.png" &
fi

pgrep -x flameshot >/dev/null 2>&1 || flameshot &

