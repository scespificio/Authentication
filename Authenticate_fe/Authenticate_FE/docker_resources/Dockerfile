# ---------- STAGE DEV : serveur Vite avec HMR ----------
FROM node:20-alpine AS dev

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# Vite en dev sur PORT
EXPOSE 5193
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5193"] 


# ---------- STAGE BUILD : build Vite ----------
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# Variables injectées au build pour Vite
ARG VITE_BACKEND_URL
ARG VITE_BACKEND_TIMEOUT
ENV VITE_BACKEND_URL=$VITE_BACKEND_URL
ENV VITE_BACKEND_TIMEOUT=$VITE_BACKEND_TIMEOUT

# Ici, Vite peut utiliser .env.prod s'il existe dans l'image,
# mais AUCUNE variable n'est passée depuis le Dockerfile.
RUN npm run build


# ---------- STAGE PROD : Nginx qui sert le build ----------
FROM nginx:1.27-alpine AS prod

# On enlève la conf par défaut
RUN rm /etc/nginx/conf.d/default.conf

# Conf nginx + entrypoint
COPY docker_resources/nginx.conf /etc/nginx/conf.d/nginx.conf
COPY docker_resources/entrypoint.sh /docker_resources/entrypoint.sh

RUN chmod +x /docker_resources/entrypoint.sh

# On copie le build Vite
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 903
ENTRYPOINT ["/docker_resources/entrypoint.sh"]
