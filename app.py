from fastapi import FastAPI
from transformers import pipeline

app = FastAPI()

# Usamos un modelo instructivo en lugar de zero-shot
generator = pipeline("text2text-generation", model="google/flan-t5-large")

@app.post("/clasificar")
def clasificar(texto: str):
    prompt = f"Clasifica el siguiente ticket de soporte TI en una categoría: {texto}"
    result = generator(prompt, max_length=50, num_return_sequences=1)
    return {
        "texto": texto,
        "categoria_generada": result[0]["generated_text"]
    }