# syntax=docker/dockerfile:1
# Base image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-alpine3.10

RUN mkdir -p /home/appuser/app

RUN pip install --upgrade pip

WORKDIR /home/appuser/app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 3000

CMD python auth.py
