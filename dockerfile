FROM python:3.11-slim

WORKDIR /app

# Dependencias del sistema
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias
COPY requeriments.txt .
RUN pip install --no-cache-dir -r requeriments.txt

# Copiar el código de la app
COPY . .

# Exponer puerto FastAPI
EXPOSE 8000

# Comando para arrancar la app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]