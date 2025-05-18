#!/bin/bash

# check uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv could not be found"
    echo "use brew or 'curl -LsSf https://astral.sh/uv/install.sh | sh' to install uv"
    exit 1
fi

if ! uv venv; then
    echo "venv could not be created"
    exit 1
fi

if ! uv pip install -r requirements.txt; then
    echo "requirements could not be installed"
    exit 1
fi

echo "setup complete"
echo
echo "run python scripts with 'uv run 0_agent.py'"
echo
exit 0
