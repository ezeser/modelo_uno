import time
from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer
from collections import defaultdict
import torch

# Inicializar FastAPI
app = FastAPI()

# Detectar si hay GPU disponible
device = 0 if torch.cuda.is_available() else -1

# Inicializar pipeline de clasificación en GPU (si existe) o CPU
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli",
    device=device
)

# Lista de categorías
CATEGORIAS = [
    "Infraestructura", "Soporte", "BI", "ITSM", "Desarrollo", "Redes", "Seguridad",
    "Correo", "Aplicación", "Base de Datos", "Hardware", "Software",
    "Accesos", "Contraseñas", "VPN", "Firewall", "Servidores",
    "Almacenamiento", "Backup", "Telefonía", "Impresoras",
    "Sistema Operativo", "Cloud", "Virtualización", "Integraciones",
    "Monitoreo", "DevOps", "Gestión de Proyectos", "Cumplimiento",
    "Usuarios", "Otro"
]

# 🔹 Variables globales para métricas
metrics = defaultdict(int)
metrics["requests_total"] = 0
metrics["tokens_in_total"] = 0
metrics["tokens_out_total"] = 0
metrics["total_time"] = 0.0

# Tokenizer para contar tokens
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-mnli")

class Ticket(BaseModel):
    texto: str

@app.post("/clasificar")
def clasificar(ticket: Ticket):
    start_time = time.time()

    # Contar tokens de entrada
    tokens_in = len(tokenizer.encode(ticket.texto))

    # Ejecutar clasificación
    result = classifier(ticket.texto, candidate_labels=CATEGORIAS)
    categoria = result["labels"][0]

    # Contar tokens de salida aproximados (categoría + labels devueltos)
    tokens_out = sum(len(tokenizer.encode(lbl)) for lbl in result["labels"])

    elapsed_time = time.time() - start_time

    # Actualizar métricas globales
    metrics["requests_total"] += 1
    metrics["tokens_in_total"] += tokens_in
    metrics["tokens_out_total"] += tokens_out
    metrics["total_time"] += elapsed_time

    return {
        "texto": ticket.texto,
        "categoria": categoria,
        "metrics": {
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "process_time": elapsed_time,
            "device": "GPU" if device == 0 else "CPU"
        }
    }

@app.get("/metrics")
def get_metrics():
    avg_time = metrics["total_time"] / metrics["requests_total"] if metrics["requests_total"] > 0 else 0
    return {
        "requests_total": metrics["requests_total"],
        "tokens_in_total": metrics["tokens_in_total"],
        "tokens_out_total": metrics["tokens_out_total"],
        "avg_response_time": avg_time,
        "device": "GPU" if device == 0 else "CPU"
    }