#!/bin/sh

[ ! -d ".venv" ] && echo "Creating .venv" && virtualenv ".venv"
source .venv/bin/activate

[ ! -f "requirements.txt" ] && pipreqs --ignore .venv
pip install -r requirements.txt && \
 pip freeze | sort -f | tee requirements.txt


# --no-cache
docker build -t pufe97/persons-app-api:latest . && \
 docker push pufe97/persons-app-api:latest

kubectl rollout restart deployment persons-app-api && \
  kubectl get pods -o wide --watch

deactivate
docker rmi -f $(docker images --filter "dangling=true" -q --no-trunc) # cleanup dangling images#