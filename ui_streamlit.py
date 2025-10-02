import streamlit as st
import requests
import os

# ----------------------------
# Configuración de página
# ----------------------------
st.set_page_config(
    page_title="Clasificador de Tickets TI",
    layout="wide"
)

# ----------------------------
# Estilos corporativos CSS
# ----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }
    .stButton>button {
        background-color: #00FF00;
        color: #000000;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 24px;
    }
    .stButton>button:hover {
        background-color: #00cc00;
    }
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        background-color: #111111;
        color: #FFFFFF;
        border: 2px solid #00FF00;
        border-radius: 6px;
        padding: 6px;
    }
    .stContainer {
        background-color: #111111;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 0 15px #00FF00;
        margin-bottom: 20px;
    }
    hr {
        border: 1px solid #00FF00;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------
# Logo
# ----------------------------
st.markdown(
    """
    <div style='text-align:center; margin-bottom:20px;'>
        <img src="https://n.technology/wp-content/uploads/2023/03/n_technology_logo.png
