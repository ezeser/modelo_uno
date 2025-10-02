#!/usr/bin/env bash
set -e

echo "🚀 Iniciando FastAPI y Streamlit..."

# Levantar FastAPI en background
uvicorn app:app --host 0.0.0.0 --port 8000 --workers 1 &

# Esperar 5 segundos para que FastAPI esté listo
sleep 10

# Levantar Streamlit
streamlit run ui_streamlit.py --server.port=8501 --server.address=0.0.0.0

# Mantener procesos
wait
