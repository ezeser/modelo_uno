# ui_streamlit.py
import streamlit as st
import requests
import os

st.set_page_config(page_title="Clasificador de Tickets TI", layout="wide")

st.title("🛠 Clasificador de Tickets de TI")
st.markdown(
    """
Esta interfaz permite enviar tickets al microagente y obtener las categorías más relevantes.
"""
)

# Detectar automáticamente la URL de FastAPI
API_URL = st.text_input(
    "Ingrese la URL del API FastAPI",
    os.getenv("FASTAPI_URL", "http://127.0.0.1:8000/clasificar")
)

ticket_texto = st.text_area("Ingrese el texto del ticket:", height=150)

if st.button("Clasificar"):
    if ticket_texto.strip() == "":
        st.warning("Por favor ingrese un texto de ticket.")
    else:
        try:
            payload = {"texto": ticket_texto}
            response = requests.post(API_URL, json=payload)
            if response.status_code == 200:
                data = response.json()
                st.subheader("📊 Resultado de la clasificación")
                for cat in data.get("categorias", []):
                    st.write(f"**{cat['categoria']}** - Score: {cat['score']:.2f}")
                st.markdown("---")
                st.subheader("📈 Métricas")
                metrics = data.get("metrics", {})
                st.write(f"Tokens in: {metrics.get('tokens_in')}")
                st.write(f"Tokens out: {metrics.get('tokens_out')}")
                st.write(f"Tiempo de procesamiento: {metrics.get('process_time'):.2f} s")
                st.write(f"Dispositivo: {metrics.get('device')}")
            else:
                st.error(f"Error en la API: {response.status_code}")
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")
