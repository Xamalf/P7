#!/bin/bash
docker build -t auth ./auth/.
docker build -t exercise-provider ./exercise-provider/.
docker build -t exercise-verifier ./exercise-verifier/.
docker build -t website-provider ./website-provider/.

docker rm -f auth
docker rm -f exercise-provider
docker rm -f exercise-verifier
docker rm -f website-provider

docker run --name=auth -d -p 3000:3000 auth
docker run --name=exercise-provider -d -p 2000:2000 exercise-provider
docker run --name=exercise-verifier -d -p 10000:10000 exercise-verifier
docker run  --name=website-provider -d -p 4000:4000 website-provider
