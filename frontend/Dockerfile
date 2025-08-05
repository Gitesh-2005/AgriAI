FROM node:20.19.4-alpine3.21

WORKDIR /AGRIAI

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host"]
