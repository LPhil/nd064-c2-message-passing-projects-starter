#!/bin/sh

[ ! -d ".venv" ] && echo "Creating .venv" && virtualenv ".venv"
source .venv/bin/activate

[ ! -f "requirements.txt" ] && pipreqs --ignore .venv
pip install -r requirements.txt && \
 pip freeze | grep -v file: | sort -f | tee requirements.txt

rmdir dist > /dev/null 2>&1
mkdir dist > /dev/null 2>&1
cp -rf ../UdaDB/dist .

# --no-cache
docker build -t pufe97/persons-api:latest . && \
 docker push pufe97/persons-api:latest

kubectl rollout restart deployment persons-api && \
  kubectl get pods -o wide --watch

deactivate
docker rmi -f $(docker images --filter "dangling=true" -q --no-trunc) # cleanup dangling images#