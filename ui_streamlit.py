import streamlit as st
import requests
import os

# ----------------------------
# Configuración de página
# ----------------------------
st.set_page_config(page_title="Clasificador de Tickets TI", layout="wide")

# ----------------------------
# Estilos CSS personalizados
# ----------------------------
st.markdown(
    """
    <style>
    /* Fondo oscuro elegante */
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        color: #FFFFFF;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Contenedor principal con glassmorphism */
    .block-container {
        background: rgba(20, 20, 20, 0.85);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        padding: 30px;
        border-radius: 16px;
        box-shadow: 0 8px 32px 0 rgba(0, 255, 0, 0.2);
    }

    /* Títulos con efecto neon */
    h1, h2, h3 {
        color: #00FF88 !important;
        text-shadow: 0 0 8px #00FF88, 0 0 12px #00FF88;
    }

    /* Botones con efecto hover */
    .stButton>button {
        background: linear-gradient(90deg, #00FF88, #00cc66);
        color: black;
        font-weight: bold;
        border-radius: 10px;
        padding: 12px 28px;
        border: none;
        box-shadow: 0px 0px 15px #00FF88;
        transition: all 0.3s ease-in-out;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #00cc66, #009944);
        transform: scale(1.05);
        box-shadow: 0px 0px 25px #00FF88;
    }

    /* Inputs elegantes */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background: rgba(30, 30, 30, 0.9);
        color: #FFFFFF;
        border: 2px solid #00FF88;
        border-radius: 8px;
        padding: 8px;
        font-size: 14px;
    }

    /* Separadores */
    hr {
        border: 1px solid #00FF88;
        margin: 25px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Encabezado
# ----------------------------
st.markdown("<h1 style='text-align:center;'>🛠 Clasificador de Tickets de TI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Interfaz para enviar tickets al microagente y obtener categorías relevantes</p>", unsafe_allow_html=True)

# ----------------------------
# Contenido de la UI
# ----------------------------
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
