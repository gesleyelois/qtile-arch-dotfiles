#!/usr/bin/env bash
set -euo pipefail

venv_dir="$HOME/.local/share/mypy-venv"
bin_dir="$HOME/.local/bin"

python -m venv "$venv_dir"
"$venv_dir/bin/python" -m pip install --upgrade pip mypy

mkdir -p "$bin_dir"

cat >"$bin_dir/mypy" <<'SCRIPT'
#!/bin/sh
system_site="$(/usr/bin/python -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])' 2>/dev/null || true)"
if [ -n "$system_site" ]; then
    export PYTHONPATH="${system_site}${PYTHONPATH:+:$PYTHONPATH}"
fi
exec "$HOME/.local/share/mypy-venv/bin/python" -m mypy "$@"
SCRIPT

cat >"$bin_dir/stubtest" <<'SCRIPT'
#!/bin/sh
system_site="$(/usr/bin/python -c 'import sysconfig; print(sysconfig.get_paths()["purelib"])' 2>/dev/null || true)"
if [ -n "$system_site" ]; then
    export PYTHONPATH="${system_site}${PYTHONPATH:+:$PYTHONPATH}"
fi
exec "$HOME/.local/share/mypy-venv/bin/python" -m mypy.stubtest "$@"
SCRIPT

chmod +x "$bin_dir/mypy" "$bin_dir/stubtest"

echo "Fixed mypy and stubtest wrappers in $bin_dir"
