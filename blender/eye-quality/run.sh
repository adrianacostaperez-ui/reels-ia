#!/usr/bin/env bash
set -euo pipefail
mode="${1:-check_environment}"
if [ "$#" -gt 0 ]; then shift; fi
case "$mode" in check_environment|generate_textures|create_scene|render_frames|interpolate|package_scene|validate) ;; *) echo "Unknown Blender task" >&2; exit 2;; esac
export BLENDER_USER_CONFIG=/workspace/blender-user
export XDG_CONFIG_HOME=/workspace/blender-xdg
export XDG_CACHE_HOME=/workspace/blender-cache
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec /workspace/blender-python/bin/python "$script_dir/$mode.py" -- "$@"
