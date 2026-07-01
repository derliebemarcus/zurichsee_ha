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
    requirementsFile: 'requirements-dev.txt',
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
        mode: 'container',
        image: 'registry.home.siczb.de/siczb/python-ci:latest',
        engine: 'podman',
        shell: '/bin/bash',
        pullPolicy: 'never',
        keepId: true,
    ],
    workspaceNormalizationCommand: '''
        set +e
        [ -e "$WORKSPACE" ] || exit 0
        sudo chown -R "$(id -u):$(id -g)" "$WORKSPACE" || true
        sudo chmod -R u+rwX "$WORKSPACE" || true
    ''',
    prepareCommand: 'chmod 700 tools/jenkins_prepare.sh && tools/jenkins_prepare.sh',
    commands: [
        pytest: 'chmod 700 tools/jenkins_python_tasks.sh && tools/jenkins_python_tasks.sh pytest',
        ruffLint: 'chmod 700 tools/jenkins_python_tasks.sh && tools/jenkins_python_tasks.sh ruff-lint',
        ruffFormat: 'chmod 700 tools/jenkins_python_tasks.sh && tools/jenkins_python_tasks.sh ruff-format',
        mypy: 'chmod 700 tools/jenkins_python_tasks.sh && tools/jenkins_python_tasks.sh mypy',
        translations: 'chmod 700 tools/jenkins_python_tasks.sh && tools/jenkins_python_tasks.sh translations',
        pipAudit: 'chmod 700 tools/jenkins_python_tasks.sh && tools/jenkins_python_tasks.sh pip-audit',
        mutation: 'chmod 700 tools/jenkins_python_tasks.sh && tools/jenkins_python_tasks.sh mutation',
        dependencyConsistency: 'chmod 700 tools/jenkins_python_tasks.sh && tools/jenkins_python_tasks.sh dependency-consistency',
        codeql: 'chmod 700 tools/jenkins_codeql.sh && tools/jenkins_codeql.sh',
        sonar: 'chmod 700 tools/jenkins_sonar.sh && tools/jenkins_sonar.sh',
    ],
    mutation: [
        artifacts: 'reports/mutation/**,mutants/.mutmut-cache/**,.mutmut-cache',
    ],
    hassfest: [
        enabled: true,
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
