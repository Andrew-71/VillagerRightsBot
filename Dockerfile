FROM node:16-alpine

WORKDIR /usr/src/app

COPY package*.json ./
COPY . .
RUN npm install
RUN npm prune --production

# Deploy the commands and run the app
CMD [ "node", "deploy-commands.js" ]
CMD [ "node", "main.js" ]