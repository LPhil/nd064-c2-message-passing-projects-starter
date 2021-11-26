#!/bin/sh

kubectl delete ns udaconnect
kubectl create ns udaconnect

helm repo add bitnami https://charts.bitnami.com/bitnami
helm install kafka-broker -f Helm/kafka-zookeeper-values.yaml bitnami/kafka -n udaconnect
sleep 25 # For productive operation, a dependency between containers should be implemented with spec.initContainers.

kubectl apply -f deployment/Kubernetes/ -n udaconnect
kubectl get deployments.apps -n udaconnect --watch
