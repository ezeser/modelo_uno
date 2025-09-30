#!/usr/bin/env bash
set -e

echo "🚀 Iniciando el microagente de tickets con FastAPI + Uvicorn..."

# Variables opcionales para configuración
WORKERS=${WORKERS:-1}
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}

# Lanzar Uvicorn con workers y autoreload solo si estamos en dev
if [ "$ENV" = "dev" ]; then
    exec uvicorn app:app --host $HOST --port $PORT --reload
else
    exec uvicorn app:app --host $HOST --port $PORT --workers $WORKERS
fi
