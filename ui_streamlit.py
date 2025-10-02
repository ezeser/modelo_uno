import streamlit as st
import requests
import os
import base64

# ----------------------------
# Configuración de página
# ----------------------------
st.set_page_config(page_title="Clasificador de Tickets TI", layout="wide")

# ----------------------------
# Función para cargar imagen como base64
# ----------------------------
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(f.read()).decode()

# Convierte tu imagen
img_base64 = get_base64_of_bin_file("NTechCover_Screen-3.png")

# ----------------------------
# CSS con Glassmorphism
# ----------------------------
st.markdown(
    f"""
    <style>
    /* Fondo general con imagen */
    .stApp {{
        background: url("data:image/png;base64,{img_base64}") no-repeat center center fixed;
        background-size: cover;
        color: #FFFFFF;
        font-family: 'Segoe UI', sans-serif;
    }}

    /* Bloques flotantes tipo "glassmorphism" */
    .block-container {{
        background: rgba(0, 0, 0, 0.6);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 8px 32px 0 rgba(0, 255, 0, 0.37);
    }}

    /* Logo centrado */
    .logo {{
        display: flex;
        justify-content: center;
        margin-bottom: 20px;
    }}

    /* Títulos con efecto neon */
    h1, h2, h3 {{
        color: #00FF00 !important;
        text-shadow: 0 0 10px #00FF00, 0 0 20px #00FF00;
    }}

    /* Botones */
    .stButton>button {{
        background: linear-gradient(90deg, #00FF00, #00cc00);
        color: black;
        font-weight: bold;
        border-radius: 10px;
        padding: 12px 28px;
        border: none;
        box-shadow: 0px 0px 15px #00FF00;
        transition: all 0.3s ease-in-out;
    }}
    .stButton>button:hover {{
        background: linear-gradient(90deg, #00cc00, #009900);
        transform: scale(1.05);
        box-shadow: 0px 0px 25px #00FF00;
    }}

    /* Inputs */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {{
        background: rgba(17, 17, 17, 0.8);
        color: #FFFFFF;
        border: 2px solid #00FF00;
        border-radius: 8px;
        padding: 8px;
        font-size: 14px;
    }}

    /* Separadores */
    hr {{
        border: 1px solid #00FF00;
        margin: 25px 0;
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
        <img src="https://n.technology/wp-content/uploads/2023/03/n_technology_logo.png" width="220">
    </div>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Contenido UI
# ----------------------------
st.markdown("## 🛠 Clasificador de Tickets de TI")
st.markdown("Interfaz moderna para enviar tickets al microagente y obtener categorías relevantes con métricas detalladas.")

with st.container():
    API_URL = st.text_input(
        "🔗 Ingrese la URL del API FastAPI",
        os.getenv("FASTAPI_URL", "http://127.0.0.1:8000/clasificar")
    )
    ticket_texto = st.text_area("📝 Ingrese la descripción del ticket:", height=150)

    if st.button("🚀 Clasificar Ticket"):
        if ticket_texto.strip() == "":
            st.warning("⚠️ Por favor ingrese un texto de ticket.")
        else:
            try:
                payload = {"texto": ticket_texto}
                response = requests.post(API_URL, json=payload, timeout=120)
                if response.status_code == 200:
                    data = response.json()
                    st.markdown("### 📊 Resultado de la clasificación")
                    for cat in data.get("categorias", []):
                        st.success(f"✅ **{cat['categoria']}** - Score: {cat['score']:.2f}")
                    st.markdown("---")
                    st.markdown("### 📈 Métricas")
                    metrics = data.get("metrics", {})
                    st.info(f"🔹 Tokens in: {metrics.get('tokens_in')}")
                    st.info(f"🔹 Tokens out: {metrics.get('tokens_out')}")
                    st.info(f"⏱ Tiempo de procesamiento: {metrics.get('process_time'):.2f} s")
                    st.info(f"💻 Dispositivo: {metrics.get('device')}")
                else:
                    st.error(f"❌ Error en la API: {response.status_code}")
            except Exception as e:
                st.error(f"⚠️ Ocurrió un error: {e}")
