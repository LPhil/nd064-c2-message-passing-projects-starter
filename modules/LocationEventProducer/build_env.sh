#!/bin/zsh

[ ! -d ".venv" ] && echo "Creating .venv" && virtualenv ".venv"
source .venv/bin/activate
pip install -r requirements.txt
pip freeze | sort | tee requirements.txt
#pip install --upgrade pip
#pip install -r requirements.txt

# --no-cache
docker build -t pufe97/locationevent-producer:latest . && \
 docker push pufe97/locationevent-producer:latest
