#!/bin/sh

python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./proto/locationevent.proto

[ ! -d ".venv" ] && echo "Creating .venv" && virtualenv ".venv"
source .venv/bin/activate

[ ! -f "requirements.txt" ] && pipreqs --ignore .venv
pip install -r requirements.txt && \
 pip freeze | sort -f | tee requirements.txt


# --no-cache
docker build -t pufe97/locationevent-producer:latest . && \
 docker push pufe97/locationevent-producer:latest

kubectl rollout restart deployment locationevent-producer && \
  kubectl get pods -o wide --watch

deactivate
docker rmi -f $(docker images --filter "dangling=true" -q --no-trunc) # cleanup dangling images