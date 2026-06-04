import streamlit as st
from problemas import gato, reinas, frozen_lake, sokoban # Importaremos los demás después

st.set_page_config(page_title="Visualizador de Búsqueda IA", layout="wide")

st.title("Visualizador de Algoritmos de Búsqueda")

# Menú lateral
st.sidebar.header("Configuración")
problema_seleccionado = st.sidebar.selectbox(
    "Selecciona el problema:",
    [
        "Gato / Tic-Tac-Toe (Adversaria)", 
        "8 Reinas (Local)", 
        "Frozen Lake (No informada)", 
        "Sokoban (Informada)"
    ]
)

st.write("---")

# Enrutador
if problema_seleccionado == "Gato / Tic-Tac-Toe (Adversaria)":
    gato.mostrar_interfaz()
elif problema_seleccionado == "8 Reinas (Local)":
    reinas.mostrar_interfaz()
elif problema_seleccionado == "Frozen Lake (No informada)":
    frozen_lake.mostrar_interfaz()
elif problema_seleccionado == "Sokoban (Informada)":
    sokoban.mostrar_interfaz()