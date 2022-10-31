#!/bin/bash
docker build -t auth ./auth/.
docker build -t exercise-provider ./exercise-provider/.
docker build -t exercise-verifier ./exercise-verifier/.
docker build -t website-provider ./website-provider/.

docker run -d -p 3000:3000 auth
docker run -d -p 2000:2000 exercise-provider
docker run -d -p 10000:10000 exercise-verifier
docker run -d -p 4000:4000 website-provider
