from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

# Inicializar API
app = FastAPI()

# Modelo generativo
generator = pipeline("text2text-generation", model="google/flan-t5-base")

class Ticket(BaseModel):
    texto: str

@app.post("/clasificar")
def clasificar(ticket: Ticket):
    prompt = (
        "Analiza el siguiente reporte de usuario y genera una categoría breve y clara de TI. "
        "Responde en formato JSON con la clave 'categoria'.\n\n"
        f"Texto: {ticket.texto}\n\n"
        "Respuesta:"
    )

    result = generator(prompt, max_length=50, do_sample=False, num_return_sequences=1)
    raw_output = result[0]["generated_text"]

    return {
        "texto": ticket.texto,
        "categoria_generada": raw_output.strip()
    }
