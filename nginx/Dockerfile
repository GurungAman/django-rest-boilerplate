# FROM node:16.14.2-alpine3.14 as build

# RUN mkdir -p /usr/src/app
# WORKDIR /usr/src/app

# COPY package.json package-lock.json .dockerignore ./

# COPY . .

# RUN npm run build

# The second stage
# Copy React static files and start nginx

FROM nginx:1.23-alpine
# COPY --from=build /usr/src/app/build /var/www/html

CMD ["nginx", "-g", "daemon off;"]