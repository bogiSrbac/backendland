FROM node:16.13.0

WORKDIR /code

ENV PORT 80

COPY json/package.json /code/package.json

RUN npm install
RUN npm install amqplib
RUN npm install -g nodemon
RUN npm install socket.io
RUN npm install socket.io-client
RUN npm install uuid

COPY . /code

EXPOSE 666

CMD ["node", "server.js", "hocusMessanger.js"]
