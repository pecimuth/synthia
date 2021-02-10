FROM node:12
WORKDIR /app
COPY . .
EXPOSE 4200
EXPOSE 49153
RUN npm ci
CMD npm run ng -- serve --host=0.0.0.0 --port=4200 --poll 5000
