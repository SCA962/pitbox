# Usa una imagen oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de dependencias
COPY ./requirements.txt /app/requirements.txt

# Instala las dependencias
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copia el código fuente de la aplicación de forma específica
COPY ./app /app/app

# Expone el puerto que usará la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación con recarga automática
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
