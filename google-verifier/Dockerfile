FROM node:alpine

RUN mkdir -p /home/appuser/app

RUN npm install npm@latest -g

WORKDIR /home/appuser/app

COPY requirements.txt requirements.txt

RUN cat requirements.txt | xargs npm install -g

COPY . .

EXPOSE 6000

CMD ["node", "google-verifier.js", ">", "logs"]
