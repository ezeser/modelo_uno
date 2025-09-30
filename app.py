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

# Modelo más ligero recomendado
MODEL_NAME = "facebook/bart-large-mnli"  # Más liviano que Mistral
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

    # Prompts contextuales
    prompts = [
        f"Clasifica este ticket de TI: {ticket.texto}",
        f"Qué categoría de soporte de TI describe mejor esto: {ticket.texto}?",
        f"El siguiente mensaje pertenece a un ticket de soporte técnico, identifica sus categorías principales: {ticket.texto}"
    ]

    # Clasificar con cada prompt
    scores = defaultdict(float)
    for p in prompts:
        result = classifier(p, candidate_labels=CATEGORIAS)
        for lbl, score in zip(result["labels"], result["scores"]):
            scores[lbl] += score  # Sumar scores para ponderar

    # Obtener top 3 finales (ordenadas por relevancia)
    top3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]

    # Convertir a escalera mostrando el nombre real de la categoría
    top3_escalera = [
        {"categoria": lbl, "nivel": f"Categoria {i+1}", "score": float(score)}
        for i, (lbl, score) in enumerate(top3)
    ]

    tokens_out = sum(len(tokenizer.encode(lbl)) for lbl, _ in top3)
    elapsed_time = time.time() - start_time

    # Actualizar métricas
    metrics["requests_total"] += 1
    metrics["tokens_in_total"] += tokens_in
    metrics["tokens_out_total"] += tokens_out
    metrics["total_time"] += elapsed_time

    return {
        "texto": ticket.texto,
        "categorias": top3_escalera,
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
