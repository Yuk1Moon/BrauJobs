#!/usr/bin/env bash
set -euo pipefail
PORT="${PORT:-8000}"
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"
echo "Sirviendo Changes Hair en http://localhost:${PORT} (Ctrl+C para salir)"
python -m http.server "$PORT"
