#!/bin/bash
eval $(minikube -p minikube docker-env)
minikube addons enable ingress

docker build -t exercise-provider ./exercise-provider/.
kubectl delete -f ./exercise-provider/exercise-provider.yaml
kubectl apply -f ./exercise-provider/exercise-provider.yaml

docker build -t google-verifier ./google-verifier/.
kubectl delete -f ./google-verifier/google-verifier.yaml
kubectl apply -f ./google-verifier/google-verifier.yaml

docker build -t exercise-verifier ./exercise-verifier/.
kubectl delete -f ./exercise-verifier/exercise-verifier.yaml
kubectl apply -f ./exercise-verifier/exercise-verifier.yaml

docker build -t website-provider ./website-provider/.
kubectl delete -f ./website-provider/website-provider.yaml
kubectl apply -f ./website-provider/website-provider.yaml

docker build -t data-access ./data-access/. --no-cache
kubectl delete -f ./data-access/data-access.yaml
kubectl apply -f ./data-access/data-access.yaml

kubectl delete -f ./databases/user_db.yaml
kubectl apply -f ./databases/user_db.yaml

kubectl apply -f ./databases/volumeandclaim.yaml

docker build -t auth ./auth/.
kubectl delete -f ./auth/auth.yaml
kubectl apply -f ./auth/auth.yaml

kubectl apply -f ./secrets/db_secret.yaml
kubectl apply -f ./secrets/google_secret.yaml

kubectl delete -f ./ingress.yaml
kubectl apply -f ./ingress.yaml
