#!/bin/bash
eval $(minikube -p minikube docker-env)

docker build -t auth ./auth/. --no-cache
docker build -t exercise-provider ./exercise-provider/. --no-cache
docker build -t exercise-verifier ./exercise-verifier/. --no-cache
docker build -t website-provider ./website-provider/. --no-cache

kubectl delete -f ./auth/auth.yaml
kubectl delete -f ./exercise-provider/exercise-provider.yaml
kubectl delete -f ./exercise-verifier/exercise-verifier.yaml
kubectl delete -f ./website-provider/website-provider.yaml
kubectl delete -f ./ingress.yaml

kubectl apply -f ./auth/auth.yaml
kubectl apply -f ./exercise-provider/exercise-provider.yaml
kubectl apply -f ./exercise-verifier/exercise-verifier.yaml
kubectl apply -f ./website-provider/website-provider.yaml
kubectl apply -f ./ingress.yaml