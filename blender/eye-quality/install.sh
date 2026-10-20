#!/usr/bin/env bash
set -euo pipefail
script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [ ! -x /workspace/blender-python/bin/python ]; then
  /usr/bin/python3 -m venv --without-pip /workspace/blender-python
fi
python -m pip --python /workspace/blender-python/bin/python install -r "$script_dir/requirements.txt"
bash "$script_dir/run.sh" check_environment
