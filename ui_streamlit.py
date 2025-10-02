import streamlit as st
import requests
import os

# ----------------------------
# Configuración de página
# ----------------------------
st.set_page_config(page_title="Clasificador de Tickets TI", layout="wide")

# ----------------------------
# Estilos corporativos CSS con fondo transparente
# ----------------------------
st.markdown(
    f"""
    <style>
    /* Fondo transparente */
    .stApp {{
        background: url("NTechCover_Screen-3.png") no-repeat center center;
        background-size: cover;
        position: fixed;
        width: 100%;
        height: 100%;
        z-index: -1;
    }}

    /* Fondo semitransparente para todo el contenido */
    .stContainer, .stApp > div {{
        background-color: rgba(0, 0, 0, 0.5);  /* Semi-transparente */
        position: relative;
        z-index: 1;
        border-radius: 10px;
    }}

    /* Logo centrado */
    .logo {{
        display: flex;
        justify-content: center;
        align-items: center;
        margin-bottom: 20px;
    }}

    /* Títulos */
    .stMarkdown h1, .stMarkdown h2 {{
        color: #00FF00;
    }}

    /* Botones */
    .stButton>button {{
        background-color: #00FF00;
        color: #000000;
        border-radius: 8px;
        font-weight: bold;
        padding: 10px 24px;
    }}
    .stButton>button:hover {{
        background-color: #00cc00;
    }}

    /* Campos de entrada */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
        background-color: #111111;
        color: #FFFFFF;
        border: 2px solid #00FF00;
        border-radius: 6px;
        padding: 6px;
    }}

    /* Contenedores */
    .stContainer {{
        padding: 15px;
        box-shadow: 0 0 15px #00FF00;
        margin-bottom: 20px;
    }}

    /* Separadores */
    hr {{
        border: 1px solid #00FF00;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Logo
# ----------------------------
st.markdown(
    """
    <div class="logo">
        <img src="https://n.technology/wp-content/uploads/2023/03/n_technology_logo.png" width="200">
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Contenido de la UI
# ----------------------------
st.markdown("## 🛠 Clasificador de Tickets de TI")
st.markdown(
    """
Esta interfaz permite enviar tickets al microagente y obtener las categorías más relevantes.
""")

with st.container():
    API_URL = st.text_input(
        "Ingrese la URL del API FastAPI",
        os.getenv("FASTAPI_URL", "http://127.0.0.1:8000/clasificar")
    )
    ticket_texto = st.text_area("Ingrese la descripción del ticket:", height=150)

    if st.button("Clasificar"):
        if ticket_texto.strip() == "":
            st.warning("Por favor ingrese un texto de ticket.")
        else:
            try:
                payload = {"texto": ticket_texto}
                response = requests.post(API_URL, json=payload, timeout=120)
                if response.status_code == 200:
                    data = response.json()
                    st.markdown("### 📊 Resultado de la clasificación")
                    for cat in data.get("categorias", []):
                        st.write(f"**{cat['categoria']}** - Score: {cat['score']:.2f}")
                    st.markdown("---")
                    st.markdown("### 📈 Métricas")
                    metrics = data.get("metrics", {})
                    st.write(f"Tokens in: {metrics.get('tokens_in')}")
                    st.write(f"Tokens out: {metrics.get('tokens_out')}")
                    st.write(f"Tiempo de procesamiento: {metrics.get('process_time'):.2f} s")
                    st.write(f"Dispositivo: {metrics.get('device')}")
                else:
                    st.error(f"Error en la API: {response.status_code}")
            except Exception as e:
                st.error(f"Ocurrió un error: {e}")
