#!/usr/bin/env bash
set -euo pipefail

ROOT="$(git rev-parse --show-toplevel)"
HOOKS_DIR="$ROOT/.git/hooks"
SOURCE_DIR="$ROOT/.githooks"

if [ ! -d "$SOURCE_DIR" ]; then
  echo "Error: .githooks directory not found."
  exit 1
fi

echo "Installing git hooks..."

for hook_path in "$SOURCE_DIR"/*; do
  hook_name=$(basename "$hook_path")
  target_path="$HOOKS_DIR/$hook_name"
  
  echo "Linking $hook_name..."
  ln -sf "../../.githooks/$hook_name" "$target_path"
  chmod +x "$hook_path"
done

echo "Git hooks installed successfully."
