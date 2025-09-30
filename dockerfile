FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

WORKDIR /app

# Dependencias del sistema
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias
COPY requeriments.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la app
COPY . .

# Dar permisos al start.sh
RUN chmod +x start.sh

# Exponer puerto FastAPI
EXPOSE 8000

# Usar start.sh como entrypoint
CMD ["./start.sh"]