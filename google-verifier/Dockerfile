FROM node:alpine

RUN mkdir -p /home/appuser/app

WORKDIR /home/appuser/app

RUN npm install npm@latest -g

RUN npm install express

RUN npm install google-auth-library

# COPY requirements.txt requirements.txt

# RUN cat requirements.txt | xargs npm install -g

COPY . .

EXPOSE 6000

CMD ["node", "google-verifier.js", ">", "logs"]
