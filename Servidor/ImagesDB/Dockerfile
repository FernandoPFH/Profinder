FROM node:14.13.1-alpine3.10

COPY package-lock.json /
COPY package.json /
COPY ImagesDB.js /

COPY node_modules /node_modules

CMD ["node","ImagesDB.js"]