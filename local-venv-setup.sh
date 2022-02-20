#! /usr/bin/env bash
set -eu -o pipefail

function create-venv() {
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  deactivate
  echo "Virtual environment set up successfully"
}

create-venv