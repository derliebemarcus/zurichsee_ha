#!/usr/bin/env bash
set -euo pipefail

TAG="v0.1.5"
TARGET="878f1c4ba03b2a6b648a6ab283080d14db14c13b"

CURRENT_TARGET="$(git rev-list -n 1 "$TAG")"
if [[ "$CURRENT_TARGET" != "$TARGET" ]]; then
  echo "Tag $TAG points to $CURRENT_TARGET instead of $TARGET" >&2
  exit 1
fi

git checkout --detach "$TARGET"
python3 tools/extract_release_notes.py \
  custom_components/zurichsee_ha/manifest.json \
  CHANGELOG.md \
  release_notes.md

if gh release view "$TAG" >/dev/null 2>&1; then
  gh release edit "$TAG" \
    --title "Release $TAG" \
    --notes-file release_notes.md \
    --latest
else
  gh release create "$TAG" \
    --target "$TARGET" \
    --title "Release $TAG" \
    --notes-file release_notes.md \
    --latest
fi

git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git tag -f stable "$TARGET"
git push origin -f refs/tags/stable
