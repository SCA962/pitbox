# Etapa 1: Construcción (Node.js)
FROM node:18-alpine AS build

WORKDIR /app

# Copia package.json y package-lock.json
COPY package*.json ./

# Instala las dependencias
RUN npm install

# Copia el resto de los archivos de la aplicación
COPY . .

# Construye la aplicación para producción
RUN npm run build

# Etapa 2: Producción (Nginx)
FROM nginx:stable-alpine

# Copia los archivos construidos de la etapa anterior al directorio web de Nginx
COPY --from=build /app/dist /usr/share/nginx/html

# ¡INSTRUCCIÓN NUEVA! Copia nuestro archivo de configuración personalizado
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expone el puerto 80
EXPOSE 80

# El comando por defecto de Nginx se encargará del resto
CMD ["nginx", "-g", "daemon off;"]
