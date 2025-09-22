#!/usr/bin/env bash
set -e

echo "🚀 Iniciando el microagente de tickets..."

# Ejecutar FastAPI con Uvicorn
exec uvicorn app:app --host 0.0.0.0 --port 8000

# Nota: nunca se llega aquí porque exec reemplaza el proceso
