FROM node:20-slim AS builder
WORKDIR /app

RUN npm install -g vite

COPY frontend/package.json ./
RUN npm install

COPY frontend/src/ ./src/

WORKDIR /app/src
RUN npx vite build --config vite.config.js --outDir dist



FROM nginx:alpine

COPY frontend/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/src/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
