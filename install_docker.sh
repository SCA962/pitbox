#!/bin/bash
# Script para instalar Docker y Docker Compose en sistemas Debian/Ubuntu

# 1. Actualizar el índice de paquetes y paquetes existentes
sudo apt-get update
sudo apt-get upgrade -y

# 2. Instalar paquetes para permitir a apt usar un repositorio sobre HTTPS
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# 3. Agregar la clave GPG oficial de Docker
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# 4. Configurar el repositorio de Docker
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. Instalar Docker Engine, CLI, Containerd y Docker Compose
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 6. (Opcional) Agregar tu usuario al grupo "docker" para ejecutar comandos sin sudo
# Necesitarás cerrar sesión y volver a iniciarla para que este cambio surta efecto.
sudo usermod -aG docker $USER

# 7. Verificar la instalación
echo ""
echo "--------------------------------------------------"
echo "¡Instalación de Docker completada!"
echo "Versión de Docker:"
docker --version
echo "Versión de Docker Compose:"
docker compose version
echo ""
echo "IMPORTANTE: Cierra sesión y vuelve a iniciarla para usar Docker sin 'sudo'."
echo "--------------------------------------------------"
