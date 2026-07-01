#!/usr/bin/env bash
set -euo pipefail

python3 -m venv .venv
.venv/bin/python -m pip install \
    --disable-pip-version-check \
    --upgrade \
    pip \
    setuptools \
    wheel
.venv/bin/python -m pip install \
    --disable-pip-version-check \
    --constraint constraints.txt \
    --requirement requirements-dev.txt
