#!/bin/sh

export DB_USERNAME=ct_admin
export DB_PASSWORD=wowimsosecure
export DB_NAME=geoconnections

export DB_HOST=localhost
export DB_PORT=30050

[ -d ".venv" ] && source .venv/bin/activate

python wsgi.py
