#!/usr/bin/env bash
set -euo pipefail

output_directory="${CI_REPORT_ROOT:-reports}/codeql"
mkdir -p "$output_directory"

codeql_bin="$(command -v codeql || true)"
if [[ -z "$codeql_bin" && -n "${CODEQL_HOME:-}" ]]; then
    codeql_bin="$(find "$CODEQL_HOME" -type f -name codeql -perm -u+x | head -1)"
fi
if [[ -z "$codeql_bin" ]]; then
    echo "Unable to locate the CodeQL executable." >&2
    exit 1
fi

"$codeql_bin" version

for language in python actions; do
    database="$output_directory/db-$language"
    sarif="$output_directory/codeql-$language.sarif"
    suite="codeql/$language-queries:codeql-suites/$language-security-and-quality.qls"

    "$codeql_bin" database create "$database" \
        --language="$language" \
        --source-root=. \
        --overwrite
    "$codeql_bin" database analyze "$database" "$suite" \
        --format=sarif-latest \
        --sarif-category="$language" \
        --output="$sarif"
done
