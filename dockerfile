FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema necesarias para torch
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY requeriments.txt .

RUN pip install --no-cache-dir -r requeriments.txt

COPY . .

# Exponer puerto FastAPI.
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
