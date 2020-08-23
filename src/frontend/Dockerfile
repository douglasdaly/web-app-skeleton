## STAGE 0
FROM node:14 as build-stage

# Setup application directory
RUN mkdir /app
WORKDIR /app/

# Dependencies
COPY ./package*.json /app/
COPY ./yarn.lock /app/
RUN yarn install

# Install application
COPY ./ /app/

ARG VUE_APP_NAME=frontend
ARG VUE_APP_API_DOMAIN=localhost
ARG VUE_APP_API_PROTOCOL=https
RUN touch .env
RUN echo VUE_APP_NAME=$VUE_APP_NAME >> .env
RUN echo VUE_APP_API_DOMAIN=$VUE_APP_API_DOMAIN >> .env
RUN echo VUE_APP_API_PROTOCOL=$VUE_APP_API_PROTOCOL >> .env

RUN yarn run build


## STAGE 1
FROM nginx:1.15

COPY --from=build-stage /app/dist/ /usr/share/nginx/html

COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY ./nginx-backend-not-found.conf /etc/nginx/extra-conf.d/backend-not-found.conf
