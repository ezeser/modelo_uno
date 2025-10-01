#!/usr/bin/env bash
set -e

echo "🚀 Iniciando el microagente de tickets con FastAPI + Streamlit..."

# Variables opcionales
WORKERS=${WORKERS:-1}
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}
PORT_UI=${PORT_UI:-8501}

# Levantar FastAPI en background
if [ "$ENV" = "dev" ]; then
    uvicorn app:app --host $HOST --port $PORT --reload &
else
    uvicorn app:app --host $HOST --port $PORT --workers $WORKERS &
fi

# Levantar Streamlit en foreground
exec streamlit run ui_streamlit.py --server.port $PORT_UI --server.address $HOST
