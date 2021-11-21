#!/bin/sh

export DB_USERNAME=ct_admin
export DB_PASSWORD=wowimsosecure
export DB_NAME=geoconnections

export DB_HOST=localhost
export DB_PORT=30050


[ ! -d ".venv" ] && echo "Creating .venv" && virtualenv ".venv"
source .venv/bin/activate

#[ ! -f "requirements.txt" ] && pipreqs --ignore .venv
#pip install -r requirements.txt && \
# pip freeze | sort -f | tee requirements.txt

python wsgi.py

deactivate