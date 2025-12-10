FROM node:20-slim AS build

WORKDIR /app

COPY aht_app_frontend/habit-frontend/package.json aht_app_frontend/habit-frontend/package-lock.json ./
RUN npm install --registry=https://registry.npmjs.org/

COPY aht_app_frontend/habit-frontend/ ./
RUN npm run build

# Финальный минимальный слой
FROM nginx:alpine

COPY docker/frontend/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
