@Library('jenkins-shared-library@main') _

ciHomeAssistantIntegration(
    scm: scm,
    agentLabel: 'klymene',
    mainBranch: 'main',
    weeklyMutationCron: 'H H * * 6',
    repository: [
        owner: 'derliebemarcus',
        name: 'homeassistant_zurichsee',
    ],
    componentPath: 'custom_components/zurichsee_ha',
    manifestPath: 'custom_components/zurichsee_ha/manifest.json',
    pythonVersion: '3.14',
    pythonCommand: 'python3',
    requirementsFile: 'requirements.txt',
    constraintsFile: 'constraints.txt',
    testPaths: ['tests/unit', 'tests/ha'],
    coverageFloor: 97.1,
    reportRoot: 'reports',
    environment: [
        PYENV_ROOT: '/opt/python',
        PYENV_VERSION: '3.14',
        PATH: '/opt/python/shims:/opt/python/bin:/usr/local/bin:/usr/bin:/bin',
    ],
    runtime: [
        mode: 'host',
    ],
    prepareCommand: '''
        python3 -m venv .venv
        . .venv/bin/activate
        python3 -m pip install --disable-pip-version-check --upgrade pip setuptools wheel
        python3 -m pip install --disable-pip-version-check \
          --constraint constraints.txt \
          --requirement requirements-dev.txt
    ''',
    commands: [
        pytest: '''
            mkdir -p reports/pytest
            python3 -m pytest \
              tests/unit \
              tests/ha \
              --junitxml=reports/pytest/pytest.xml \
              --cov=custom_components/zurichsee_ha \
              --cov-config=.coveragerc \
              --cov-report=term-missing \
              --cov-report=xml:reports/pytest/coverage.xml
            python3 tools/check_coverage_threshold.py reports/pytest/coverage.xml 97.1
        ''',
        ruffLint: '''
            mkdir -p reports/ruff
            status=0
            python3 -m ruff check . --output-format=concise \
              > reports/ruff/ruff-lint.txt 2>&1 || status=$?
            cat reports/ruff/ruff-lint.txt
            exit $status
        ''',
        ruffFormat: '''
            mkdir -p reports/ruff-format
            status=0
            python3 -m ruff format --check --diff . \
              > reports/ruff-format/ruff-format.txt 2>&1 || status=$?
            cat reports/ruff-format/ruff-format.txt
            exit $status
        ''',
        mypy: '''
            mkdir -p reports/mypy
            python3 -m mypy . --junit-xml reports/mypy/mypy.xml
        ''',
        translations: '''
            mkdir -p reports/translations
            status=0
            python3 tools/check_translations.py \
              > reports/translations/check-translations.txt 2>&1 || status=$?
            cat reports/translations/check-translations.txt
            exit $status
        ''',
        pipAudit: '''
            mkdir -p reports/pip-audit
            python3 -m pip_audit \
              --requirement requirements.txt \
              --format json \
              --output reports/pip-audit/pip-audit.json \
              --ignore-vuln CVE-2026-34073 \
              --ignore-vuln CVE-2026-39892 \
              --ignore-vuln CVE-2026-25990 \
              --ignore-vuln CVE-2026-40192 \
              --ignore-vuln CVE-2026-32597 \
              --ignore-vuln CVE-2026-27448 \
              --ignore-vuln CVE-2026-27459 \
              --ignore-vuln CVE-2026-25645 \
              --ignore-vuln GHSA-pjjw-68hj-v9mw \
              --ignore-vuln CVE-2026-22815 \
              --ignore-vuln CVE-2025-67221
        ''',
        mutation: '''
            mkdir -p reports/mutation
            status=0
            python3 -m mutmut run \
              > reports/mutation/mutmut.txt 2>&1 || status=$?
            python3 -m mutmut results \
              >> reports/mutation/mutmut.txt 2>&1 || true
            cat reports/mutation/mutmut.txt
            exit $status
        ''',
        dependencyConsistency: '''
            mkdir -p reports/dependency-consistency
            status=0
            python3 -m pip check \
              > reports/dependency-consistency/pip-check.txt 2>&1 || status=$?
            cat reports/dependency-consistency/pip-check.txt
            exit $status
        ''',
    ],
    mutation: [
        artifacts: 'reports/mutation/**,.mutmut-cache',
    ],
    hassfest: [
        enabled: false,
    ],
    sonar: [
        enabled: true,
        server: 'SonarQube',
        projectKey: 'zurichsee_ha',
        projectName: 'Zürichsee Home Assistant Integration',
        timeoutMinutes: 15,
    ],
    coveralls: [
        enabled: true,
        file: 'reports/pytest/coverage.xml',
        credentialId: 'Coveralls',
        runtime: 'host',
    ],
    repositoryChecks: [
        commitMessageScript: 'tools/check_commit_messages.py',
        releaseNoteScript: 'tools/check_release_notes.py',
        changelog: 'CHANGELOG.md',
    ],
    security: [
        gitleaks: [enabled: true],
        trivy: [enabled: true],
        codeql: [
            enabled: true,
            toolName: 'codeql',
            toolPath: 'codeql',
            languages: ['python', 'actions'],
        ],
        osv: [enabled: true],
        actionlint: [enabled: true],
    ],
    github: [
        credentialId: 'github token',
        publishStageChecks: true,
        publishFinalCheck: false,
        statusContext: 'Continuous Integration / Jenkins',
        title: 'Zürichsee Quality Gates',
    ],
    homeAssistant: [
        enabled: true,
    ],
)
