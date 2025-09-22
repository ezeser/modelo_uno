FROM python:3.11-slim

# Crear directorio de trabajo
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

# Exponer puerto FastAPI
EXPOSE 8000

# Arrancar FastAPI con uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]