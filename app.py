from fastapi import FastAPI
from transformers import pipeline

app = FastAPI()

# Modelo generativo de instrucciones
classifier = pipeline("text2text-generation", model="google/flan-t5-base")

@app.get("/")
def home():
    return {"message": "API de clasificación de tickets lista"}

@app.post("/clasificar")
def clasificar(texto: str):
    prompt = f"Clasifica el siguiente ticket de soporte en una categoría de tecnologia\n\nTicket: {texto}\n\nCategoría:"
    result = classifier(prompt, max_length=50, do_sample=False)
    return {
        "texto": texto,
        "categoria_generada": result[0]["generated_text"].strip()
    }
