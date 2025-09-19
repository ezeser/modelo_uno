from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

# Modelo generativo (puedes cambiar por otro instruct más grande si quieres)
generator = pipeline("text2text-generation", model="google/flan-t5-base")

class Ticket(BaseModel):
    texto: str

# Listado de categorías
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
    # Construir prompt con lista de categorías
    prompt = f"""
Clasifica el siguiente texto en una de las categorías de la lista.
No inventes categorías nuevas. 
Responde solo con el nombre exacto de la categoría.

Lista de categorías: {CATEGORIAS}

Texto: "{ticket.texto}"

Categoría:
"""

    result = generator(prompt, max_length=50, do_sample=False, num_return_sequences=1)
    raw_output = result[0]["generated_text"].strip()

    return {
        "texto": ticket.texto,
        "categoria": raw_output
    }
