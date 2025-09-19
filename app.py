from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

# Inicializar pipeline zero-shot-classification
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

class Ticket(BaseModel):
    texto: str

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

@app.post("/clasificar")
def clasificar(ticket: Ticket):
    # Ejecutar zero-shot classification
    result = classifier(ticket.texto, candidate_labels=CATEGORIAS)
    
    # Devolver la categoría más probable
    categoria = result["labels"][0]
    
    return {
        "texto": ticket.texto,
        "categoria": categoria
    }
