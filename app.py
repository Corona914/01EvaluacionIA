import streamlit as st
from streamlit_option_menu import option_menu
from problemas import gato, reinas, frozen_lake, sokoban # Importaremos los demás después

st.set_page_config(page_title="Visualizador de Búsqueda IA", layout="wide")

st.title("Visualizador de Algoritmos de Búsqueda")


with st.sidebar:
    st.title("🧠 Algoritmos IA")
    st.markdown("---")
    
    problema_seleccionado = option_menu(
        menu_title=None,
        options=[
            "Gato / Tic-Tac-Toe (Adversaria)", 
            "8 Reinas (Local)", 
            "Frozen Lake (No informada)", 
            "Sokoban (Informada)"
        ],
        icons=["grid-3x3", "puzzle", "snow", "box-seam"], 
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"font-size": "18px", "color": "#a8b2c1"}, 
            "nav-link": {
                "font-size": "16px", 
                "text-align": "left", 
                "margin": "0px", 
                "--hover-color": "rgba(255,255,255,0.05)"
            },
            "nav-link-selected": {"background-color": "rgba(255,255,255,0.1)", "color": "white"},
        }
    )
    
    st.markdown("---")

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