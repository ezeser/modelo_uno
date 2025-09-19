from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import json

# Inicializar API
app = FastAPI()

# Modelo generativo
generator = pipeline("text2text-generation", model="google/flan-t5-base")

class Ticket(BaseModel):
    texto: str

@app.post("/clasificar")
def clasificar(ticket: Ticket):
    prompt = (
        "Clasifica el siguiente reporte de usuario en una categoría breve de TI.\n"
        "Devuelve SOLO un JSON válido con la clave 'categoria'.\n\n"
        f"Texto: {ticket.texto}\n\n"
        "JSON:"
    )

    result = generator(prompt, max_length=50, do_sample=False, num_return_sequences=1)
    raw_output = result[0]["generated_text"].strip()

    # Intentar parsear JSON, si falla devolver texto crudo
    try:
        parsed = json.loads(raw_output)
        categoria = parsed.get("categoria", raw_output)
    except Exception:
        categoria = raw_output

    return {
        "texto": ticket.texto,
        "categoria_generada": categoria
    }
