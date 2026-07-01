#!/usr/bin/env bash
set -euo pipefail

task="${1:-}"
python="${PYTHON:-.venv/bin/python}"
report_root="${CI_REPORT_ROOT:-reports}"

case "$task" in
    pytest)
        mkdir -p "$report_root/pytest"
        "$python" -m pytest tests/unit tests/ha \
            --junitxml="$report_root/pytest/pytest.xml" \
            --cov=custom_components/zurichsee_ha \
            --cov-config=.coveragerc \
            --cov-report=term-missing \
            --cov-report="xml:$report_root/pytest/coverage.xml"
        "$python" tools/check_coverage_threshold.py \
            "$report_root/pytest/coverage.xml" 97.1
        "$python" tools/build_release_asset.py \
            "$report_root/pytest/zurichsee_ha.zip"
        test -s "$report_root/pytest/zurichsee_ha.zip"
        ;;
    ruff-lint)
        mkdir -p "$report_root/ruff"
        "$python" -m ruff check . \
            --output-format=json \
            --output-file="$report_root/ruff/ruff-report.json"
        ;;
    ruff-format)
        mkdir -p "$report_root/ruff-format"
        status=0
        "$python" -m ruff format --check --diff . \
            > "$report_root/ruff-format/ruff-format.txt" 2>&1 || status=$?
        cat "$report_root/ruff-format/ruff-format.txt"
        exit "$status"
        ;;
    mypy)
        mkdir -p "$report_root/mypy"
        "$python" -m mypy . \
            --junit-xml "$report_root/mypy/mypy.xml"
        ;;
    translations)
        mkdir -p "$report_root/translations"
        status=0
        "$python" tools/check_translations.py \
            > "$report_root/translations/translations.txt" 2>&1 || status=$?
        cat "$report_root/translations/translations.txt"
        exit "$status"
        ;;
    pip-audit)
        mkdir -p "$report_root/pip-audit"
        audit_args=(
            --requirement requirements.txt
            --format json
            --output "$report_root/pip-audit/pip-audit-report.json"
        )
        while IFS= read -r advisory || [[ -n "$advisory" ]]; do
            advisory="${advisory%%#*}"
            advisory="${advisory#"${advisory%%[![:space:]]*}"}"
            advisory="${advisory%"${advisory##*[![:space:]]}"}"
            [[ -z "$advisory" ]] && continue
            audit_args+=(--ignore-vuln "$advisory")
        done < tools/pip-audit-ignore.txt
        "$python" -m pip_audit "${audit_args[@]}"
        ;;
    mutation)
        mkdir -p "$report_root/mutation"
        rm -rf mutants
        status=0
        "$python" -m mutmut run \
            > "$report_root/mutation/mutmut.txt" 2>&1 || status=$?
        "$python" -m mutmut results \
            >> "$report_root/mutation/mutmut.txt" 2>&1 || true
        cat "$report_root/mutation/mutmut.txt"
        exit "$status"
        ;;
    dependency-consistency)
        mkdir -p "$report_root/dependency-consistency"
        status=0
        "$python" -m pip check \
            > "$report_root/dependency-consistency/pip-check.txt" 2>&1 || status=$?
        cat "$report_root/dependency-consistency/pip-check.txt"
        exit "$status"
        ;;
    *)
        echo "Unknown Python quality task: $task" >&2
        exit 2
        ;;
esac
