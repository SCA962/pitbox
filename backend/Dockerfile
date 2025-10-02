# Usa una imagen oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia el archivo de dependencias
COPY ./requirements.txt /app/requirements.txt

# Instala las dependencias
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copia el resto de la aplicación
COPY . /app

# Expone el puerto que usará la aplicación
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
