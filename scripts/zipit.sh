#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
DIST_DIR="$PROJECT_DIR/dist"
ZIP_BASENAME="${1:-g900-force-compression-overleaf.zip}"
ZIP_PATH="$DIST_DIR/$ZIP_BASENAME"

echo "[info] project directory: $PROJECT_DIR"
echo "[info] output directory: $DIST_DIR"
echo "[info] creating Overleaf zip: $ZIP_PATH"

if ! command -v zip >/dev/null 2>&1; then
  echo "[error] zip command not found."
  echo "On Termux, run: pkg install zip -y"
  exit 1
fi

mkdir -p "$DIST_DIR"
rm -f "$ZIP_PATH"

cd "$PROJECT_DIR"

zip -r "$ZIP_PATH" \
  main.tex \
  sections \
  refs \
  figures \
  notes \
  -x \
  "build/*" \
  "dist/*" \
  "*.aux" \
  "*.bbl" \
  "*.bcf" \
  "*.blg" \
  "*.fdb_latexmk" \
  "*.fls" \
  "*.log" \
  "*.out" \
  "*.run.xml" \
  "*.synctex.gz" \
  "*.toc" \
  "*.lof" \
  "*.lot" \
  "*.nav" \
  "*.snm" \
  "*.vrb" \
  "*.xdv" \
  "*.pdf" \
  ".git/*" \
  ".DS_Store"

echo "[ok] wrote $ZIP_PATH"
ls -lh "$ZIP_PATH"

echo
echo "[info] zip contents:"
unzip -l "$ZIP_PATH"
