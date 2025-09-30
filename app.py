import time
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline, AutoTokenizer
from collections import defaultdict
import torch

# Inicializar FastAPI
app = FastAPI()

# Detectar GPU
device = 0 if torch.cuda.is_available() else -1

# Inicializar pipeline con Mistral (mejor para clasificación más precisa)
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"
classifier = pipeline(
    "zero-shot-classification",
    model=MODEL_NAME,
    device=device
)

# Categorías predefinidas
CATEGORIAS = [
    "Infraestructura", "Soporte", "BI", "ITSM", "Desarrollo", "Redes", "Seguridad",
    "Correo", "Aplicación", "Base de Datos", "Hardware", "Software",
    "Accesos", "Contraseñas", "VPN", "Firewall", "Servidores",
    "Almacenamiento", "Backup", "Telefonía", "Impresoras",
    "Sistema Operativo", "Cloud", "Virtualización", "Integraciones",
    "Monitoreo", "DevOps", "Gestión de Proyectos", "Cumplimiento",
    "Usuarios", "Otro"
]

# Métricas globales
metrics = defaultdict(int)
metrics["requests_total"] = 0
metrics["tokens_in_total"] = 0
metrics["tokens_out_total"] = 0
metrics["total_time"] = 0.0

# Tokenizer para contar tokens
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

class Ticket(BaseModel):
    texto: str

@app.post("/clasificar")
def clasificar(ticket: Ticket):
    start_time = time.time()

    # Contar tokens de entrada
    tokens_in = len(tokenizer.encode(ticket.texto))

    # Clasificación con top-3 categorías
    result = classifier(ticket.texto, candidate_labels=CATEGORIAS)
    top3_labels = result["labels"][:3]
    top3_scores = result["scores"][:3]

    tokens_out = sum(len(tokenizer.encode(lbl)) for lbl in top3_labels)
    elapsed_time = time.time() - start_time

    # Actualizar métricas
    metrics["requests_total"] += 1
    metrics["tokens_in_total"] += tokens_in
    metrics["tokens_out_total"] += tokens_out
    metrics["total_time"] += elapsed_time

    return {
        "texto": ticket.texto,
        "categorias": [
            {"label": top3_labels[i], "score": float(top3_scores[i])}
            for i in range(3)
        ],
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
