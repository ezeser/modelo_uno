from fastapi import FastAPI
from transformers import pipeline

# Inicializar API
app = FastAPI()

# Cargar modelo
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
categorias = ["Correo", "Red", "Aplicación"]

@app.get("/")
def home():
    return {"message": "API de clasificación de tickets lista "}

@app.post("/clasificar")
def clasificar(texto: str):
    result = classifier(texto, candidate_labels=categorias)
    return {
        "texto": texto,
        "categoria_predicha": result["labels"][0],
        "score": result["scores"][0]
    }
