import streamlit as st
import time
from problemas.algoritmos.busqueda_no_informada import busqueda_bfs, busqueda_dfs

MAPA_4x4 = [
    ['S', 'F', 'F', 'F'],
    ['F', 'H', 'F', 'H'],
    ['F', 'F', 'F', 'G'],
    ['H', 'F', 'F', 'F']
]

FILAS = len(MAPA_4x4)
COLUMNAS = len(MAPA_4x4[0])
INICIO = (0, 0)

# Diccionario para hacer la interfaz más visual
ICONOS = {
    'S': "🧊", 
    'F': "❄️", 
    'H': "🕳️", 
    'G': "🎁", 
    'A': "🐧"  
}

# --- INTERFAZ STREAMLIT ---

def renderizar_mapa(posicion_agente):
    """Genera el HTML del mapa con la posición actual del agente."""
    # CSS dinámico aprovechando variables de Streamlit para ser adaptativo
    html = "<table style='border-collapse: separate; border-spacing: 8px; margin: 0 auto;'>"
    for f in range(FILAS):
        html += "<tr>"
        for c in range(COLUMNAS):
            celda = MAPA_4x4[f][c]
            contenido = ICONOS['A'] if (f, c) == posicion_agente else ICONOS[celda]
            
            # Estilo minimalista dependiente de la celda
            fondo = "background-color: var(--secondary-background-color);"
            if celda == 'H': fondo = "background-color: rgba(255, 75, 75, 0.15);"
            elif celda == 'G': fondo = "background-color: rgba(75, 255, 75, 0.15);"
            
            html += f"<td style='width: 75px; height: 75px; {fondo} text-align: center; font-size: 35px; border-radius: 16px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); transition: transform 0.2s ease;'>{contenido}</td>"
        html += "</tr>"
    html += "</table>"
    return html

def mostrar_interfaz():
    st.title("🧊 Frozen Lake")
    st.markdown("---")

    col_info, col_mapa = st.columns([1, 2])

    with col_info:
        st.markdown(
            "Ayuda al pingüino 🐧 a llegar al regalo 🎁.<br>"
            "Cruza el hielo ❄️ y evita los agujeros 🕳️.",
            unsafe_allow_html=True
        )
        st.write("")
        
        st.markdown("##### ⚙️ Algoritmo")
        # Selectbox en lugar de radio para ahorrar espacio (minimalista)
        algoritmo = st.selectbox("Alg", ["BFS (Garantiza ruta corta)", "DFS (Búsqueda profunda)"], label_visibility="collapsed")
        
        velocidad = 0.75
        
        st.write("")
        ejecutar = st.button("🚀 Iniciar", type="primary", use_container_width=True)
        st.write("")
        
        # Aquí se mostrarán resultados o métricas
        info_placeholder = st.empty()

    with col_mapa:
        # Contenedor para el mapa HTML centrado vertical y horizontalmente
        st.write("") 
        mapa_placeholder = st.empty()
        mapa_placeholder.markdown(renderizar_mapa(INICIO), unsafe_allow_html=True)

    if ejecutar:
        info_placeholder.info("⏳ Calculando ruta óptima...")
        
        if "BFS" in algoritmo:
            camino, nodos = busqueda_bfs(MAPA_4x4, INICIO)
        else:
            camino, nodos = busqueda_dfs(MAPA_4x4, INICIO)

        if camino:
            # Animación paso a paso
            for paso, (px, py) in enumerate(camino):
                mapa_placeholder.markdown(renderizar_mapa((px, py)), unsafe_allow_html=True)
                info_placeholder.code(f"🗺️ Paso {paso}/{len(camino)-1}\n🔍 Nodos: {nodos}")
                time.sleep(velocidad)
            
            st.toast(f"¡Meta alcanzada en {len(camino)-1} pasos!", icon="🎉")
            info_placeholder.success(f"**¡Completado!**\n\nPasos: {len(camino)-1} | Evaluación: {nodos} nodos")
        else:
            info_placeholder.error("❌ No se encontró una ruta posible.")