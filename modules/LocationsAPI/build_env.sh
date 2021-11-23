#!/bin/zsh

[ ! -d ".venv" ] && echo "Creating .venv" && virtualenv ".venv"
source .venv/bin/activate

[ ! -f "requirements.txt" ] && pipreqs --ignore .venv
pip install -r requirements.txt && \
 pip freeze | sort -f | tee requirements.txt

mkdir dist > /dev/null 2>&1 && cp -r ../UdaDB/dist .

# --no-cache
docker build -t pufe97/locations-api:latest . && \
 docker push pufe97/locations-api:latest

kubectl rollout restart deployment locations-api && \
  kubectl get pods -o wide --watch

deactivate
docker rmi -f $(docker images --filter "dangling=true" -q --no-trunc) # cleanup dangling images