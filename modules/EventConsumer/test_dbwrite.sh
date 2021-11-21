#!/bin/sh

export DB_USERNAME=ct_admin
export DB_PASSWORD=wowimsosecure
export DB_NAME=geoconnections

export DB_HOST=localhost
export DB_PORT=30050

source .venv/bin/activate
pip install -r requirements.txt

python ./app/WriteDBTest.py
deactivate