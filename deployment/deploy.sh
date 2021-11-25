#!/bin/sh

kubectl delete ns udaconnect
kubectl create ns udaconnect

# helm repo add bitnami https://charts.bitnami.com/bitnami
helm install kafka-broker -f Helm/kafka-zookeeper-values.yaml bitnami/kafka -n udaconnect
sleep 15

kubectl apply -f Kubernetes/ -n udaconnect
