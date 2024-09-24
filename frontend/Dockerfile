FROM node:22

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000

HEALTHCHECK --interval=5s --timeout=1s --retries=5 CMD curl -f http://localhost:3000 || exit 1

CMD ["npm", "run", "dev"]
