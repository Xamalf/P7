# syntax=docker/dockerfile:1
# Base image
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3-pip

RUN mkdir -p /home/appuser/app

RUN pip install --upgrade pip

WORKDIR /home/appuser/app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 10000

CMD python3 exercise-verifier.py > logs
