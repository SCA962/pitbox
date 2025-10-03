# Usa una imagen oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de dependencias PRIMERO
# Esto aprovecha la caché de Docker si las dependencias no cambian
COPY ./requirements.txt /app/requirements.txt

# Instala las dependencias
# Se usa --no-cache-dir para mantener la imagen ligera
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Ahora copia el código fuente de la aplicación
# Al copiar solo la carpeta 'app', evitamos conflictos y mantenemos la imagen limpia
COPY ./app /app/app

# Expone el puerto que usará la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación con recarga automática para desarrollo
# Apunta al 'main' dentro de la subcarpeta 'app' que creamos
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
