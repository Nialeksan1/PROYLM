# Usa la imagen oficial de Python 3.12.3
FROM python:3.12.3-slim

# Configurar variables de entorno para evitar que Python escriba archivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema necesarias para mysqlclient y otros
# Instalar el cliente de MySQL en el contenedor de Django
RUN apt-get update -y
RUN apt-get install -y python3-dev build-essential pkg-config
RUN apt-get install -y default-libmysqlclient-dev
RUN apt-get update \
&& apt-get install -y --no-install-recommends \
gcc \
libssl-dev \
curl \
lsb-release \
wget \
gnupg 
RUN apt-get update && apt-get install -y mysql-server
RUN apt-get update && apt-get upgrade -y

# Copiar el archivo requirements.txt
COPY requirements.txt /app/

# Instalar dependencias dentro del entorno virtual
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto Django
COPY . /app/

# Exponer el puerto por el que correrá Django
EXPOSE 8000
