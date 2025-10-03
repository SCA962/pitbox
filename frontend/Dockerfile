# Usar una imagen oficial y ligera de Nginx como servidor web
FROM nginx:alpine

# Copiar los archivos estáticos de nuestro frontend (HTML, CSS, JS)
# al directorio por defecto que Nginx usa para servir contenido web
COPY . /usr/share/nginx/html

# Exponer el puerto 80 (el puerto estándar para HTTP)
# docker-compose se encargará de mapear este puerto al puerto 5173 de tu máquina
EXPOSE 80
