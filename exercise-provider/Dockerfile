# syntax=docker/dockerfile:1
# Base image
FROM python:3.8-alpine

RUN mkdir -p /home/appuser/app

RUN pip install --upgrade pip

WORKDIR /home/appuser/app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 2000

CMD python exercise-provider.py > logs
