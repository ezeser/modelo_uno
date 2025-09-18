# ===============================
# Clasificación de tickets
# ===============================

!pip install transformers pandas torch --quiet

import pandas as pd
from transformers import pipeline

# 1. Cargar CSV
df = pd.read_csv("/content/tickets.csv", encoding="latin1")
print("Columnas en el CSV:", df.columns)
print(df.head())

# 2. Crear pipeline Zero-Shot
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# 3. Definir categorías posibles
categorias = ["Correo", "Red", "Aplicación"]

# 4. Probar con todos los tickets del CSV
predicciones = []
for idx, row in df.iterrows():
    texto = row["text"]  # cambia "text" si tu columna se llama diferente (ej: "subject")
    result = classifier(texto, candidate_labels=categorias)
    predicciones.append({
        "Texto": texto,
        "Categoria_Predicha": result["labels"][0],
        "Score": result["scores"][0]
    })

# 5. Guardar resultados
df_result = pd.DataFrame(predicciones)
print(df_result.head())

df_result.to_csv("/content/resultados_predicciones.csv", index=False)
print("Resultados guardados en /content/resultados_predicciones.csv")

# 6. Probar manualmente con input
while True:
    subject = input("Escribe un subject (o 'salir' para terminar): ")
    if subject.lower() == "salir":
        break
    result = classifier(subject, candidate_labels=categorias)
    print(f"Categoría: {result['labels'][0]} (confianza: {result['scores'][0]:.2f})")