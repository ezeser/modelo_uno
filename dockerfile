FROM nvidia/cuda:12.1.1-runtime-ubuntu22.04

WORKDIR /app

# Dependencias del sistema + Python
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Crear alias para python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Copiar requirements e instalar dependencias
COPY requeriments.txt .
RUN pip install --no-cache-dir -r requeriments.txt

# Copiar el código de la app (FastAPI + Streamlit + start.sh)
COPY . .

# Dar permisos al start.sh
RUN chmod +x start.sh

# Exponer puertos FastAPI (8000) y Streamlit (8501)
EXPOSE 8000
EXPOSE 8501

# Lanzar FastAPI + Streamlit en paralelo
CMD ["bash", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000 --workers 1 & streamlit run ui_streamlit.py --server.port=8501 --server.address=0.0.0.0 && wait"]

