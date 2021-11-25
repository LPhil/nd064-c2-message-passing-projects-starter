#!/bin/sh

export DB_USERNAME=ct_admin
export DB_PASSWORD=wowimsosecure
export DB_NAME=geoconnections

export DB_HOST=localhost
export DB_PORT=30050

export KAFKA_TOPIC="locations"
export KAFKA_HOST="localhost:30340"


[ ! -d ".venv_local" ] && echo "Creating .venv_local" && virtualenv ".venv_local"
source .venv_local/bin/activate
pip install -r requirements.txt

python wsgi.py

deactivate