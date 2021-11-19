#!/bin/sh

export DB_USERNAME=ct_admin
export DB_PASSWORD=wowimsosecure
export DB_NAME=geoconnections

export DB_HOST=localhost
export DB_PORT=5432
#export DB_PORT=32000

[ -d ".venv" ] && source .venv/bin/activate

#kubectl port-forward svc/postgres 5432:5432 &
python wsgi.py
