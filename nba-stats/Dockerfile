FROM node:10.15.3-jessie

RUN mkdir /app
WORKDIR /app
COPY ./package*.json /app/

RUN npm install

COPY . /app/

EXPOSE 4200
CMD ["/bin/bash"]
