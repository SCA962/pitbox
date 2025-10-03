# Etapa 1: Construcción de la aplicación React con Vite
FROM node:18-alpine AS build

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de definición de dependencias
COPY package.json package-lock.json* ./

# Instalar dependencias
# Usamos `npm ci` que es más rápido y seguro para entornos de CI/CD
RUN npm ci

# Copiar el resto del código fuente de la aplicación
COPY . .

# Construir la aplicación para producción
RUN npm run build

# Etapa 2: Servir la aplicación construida con Nginx
FROM nginx:1.25-alpine AS serve

# Copiar los archivos estáticos construidos desde la etapa anterior
# La salida de `vite build` está en la carpeta /app/dist
COPY --from=build /app/dist /usr/share/nginx/html

# Copiar la configuración personalizada de Nginx
# Sobrescribimos la configuración por defecto
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Exponer el puerto 80 para el tráfico web
EXPOSE 80

# Comando para iniciar Nginx en primer plano
CMD ["nginx", "-g", "daemon off;"]
