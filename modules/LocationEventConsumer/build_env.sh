#!/bin/zsh

[ ! -d ".venv" ] && echo "Creating .venv" && virtualenv ".venv"
source .venv/bin/activate

pip install -r requirements.txt && \
 pip install --upgrade pip

pip freeze | sort | tee requirements.txt

#pip install -r requirements.txt

# --no-cache
docker build -t pufe97/locationevent-consumer:latest . && \
 docker push pufe97/locationevent-consumer:latest

kubectl rollout restart deployment locationevent-consumer && \
  kubectl get pods -o wide --watch

deactivate
docker rmi -f $(docker images --filter "dangling=true" -q --no-trunc) # cleanup dangling images