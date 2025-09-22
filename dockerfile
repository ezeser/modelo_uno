FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para Torch/Transformers
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la app
COPY . .

# Dar permisos al start.sh
RUN chmod +x start.sh

# Exponer puerto FastAPI
EXPOSE 8000

# Usar start.sh como punto de entrada
CMD ["./start.sh"]

