#!/bin/sh

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. locationevent.proto

[ ! -d ".venv" ] && echo "Creating .venv" && virtualenv ".venv"
source .venv/bin/activate

[ ! -f "requirements.txt" ] && pipreqs --ignore .venv
pip install -r requirements.txt && \
 pip freeze | sort -f | tee requirements.txt


export DB_USERNAME=ct_admin
export DB_PASSWORD=wowimsosecure
export DB_NAME=geoconnections

export DB_HOST=localhost
export DB_PORT=30005

#kubectl port-forward svc/postgres 5432:5432 &
python wsgi.py

deactivate