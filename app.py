from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

# Modelo generativo
generator = pipeline("text2text-generation", model="google/flan-t5-base")

class Ticket(BaseModel):
    texto: str

@app.post("/clasificar")
def clasificar(ticket: Ticket):
    prompt = (
        "Analiza el siguiente reporte de usuario y clasifícalo en UNA SOLA palabra relacionada "
        "con soporte de TI (ejemplos: red, correo, aplicacion, hardware, seguridad, base_datos, sistema).\n"
        "No devuelvas frases, solo una palabra.\n\n"
        f"Texto: {ticket.texto}\n\n"
        "Categoría:"
    )

    result = generator(prompt, max_length=5, do_sample=False, num_return_sequences=1)
    raw_output = result[0]["generated_text"].strip()

    # Normalizar (evitar espacios extras o mayúsculas)
    categoria = raw_output.split()[0].lower()

    return {
        "texto": ticket.texto,
        "categoria_generada": categoria
    }
