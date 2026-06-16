import streamlit as st
import time
from problemas.algoritmos.busqueda_no_informada import busqueda_bfs, busqueda_dfs

# --- DEFINICIÓN DEL ENTORNO ---
# S: Start (Inicio), F: Frozen (Hielo/Seguro), H: Hole (Agujero), G: Goal (Meta)

NIVELES = {
    "Nivel 1 (Fácil - 4x4)": [
        ['S', 'F', 'F', 'F'],
        ['F', 'H', 'F', 'H'],
        ['F', 'F', 'F', 'G'],
        ['H', 'F', 'F', 'F']
    ],
    "Nivel 2 (Intermedio - 5x5)": [
        ['S', 'F', 'F', 'H', 'F'],
        ['F', 'H', 'F', 'F', 'F'],
        ['F', 'F', 'H', 'F', 'H'],
        ['H', 'F', 'F', 'F', 'F'],
        ['F', 'F', 'H', 'H', 'G']
    ],
    "Nivel 3 (Difícil - 6x6)": [
        ['S', 'F', 'H', 'F', 'F', 'F'],
        ['F', 'H', 'F', 'F', 'H', 'F'],
        ['F', 'F', 'F', 'H', 'F', 'F'],
        ['H', 'H', 'F', 'F', 'F', 'H'],
        ['F', 'F', 'H', 'F', 'H', 'F'],
        ['F', 'F', 'F', 'F', 'F', 'G']
    ],
    "Nivel 4 (Experto - 8x8)": [
        ['S', 'F', 'F', 'F', 'H', 'F', 'F', 'F'],
        ['F', 'H', 'F', 'H', 'F', 'F', 'H', 'F'],
        ['F', 'F', 'F', 'F', 'H', 'F', 'F', 'F'],
        ['F', 'H', 'H', 'F', 'F', 'H', 'F', 'H'],
        ['F', 'F', 'F', 'H', 'F', 'F', 'F', 'F'],
        ['H', 'F', 'H', 'F', 'F', 'H', 'H', 'F'],
        ['F', 'F', 'F', 'F', 'H', 'F', 'F', 'F'],
        ['F', 'H', 'F', 'F', 'F', 'F', 'H', 'G']
    ]
}

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

def renderizar_mapa(mapa, posicion_agente):
    """Genera el HTML del mapa dinámicamente con la posición actual del agente."""
    filas = len(mapa)
    columnas = len(mapa[0])
    
    # CSS dinámico aprovechando variables de Streamlit para ser adaptativo
    html = "<table style='border-collapse: separate; border-spacing: 8px; margin: 0 auto;'>"
    for f in range(filas):
        html += "<tr>"
        for c in range(columnas):
            celda = mapa[f][c]
            contenido = ICONOS['A'] if (f, c) == posicion_agente else ICONOS[celda]
            
            # Ajuste del tamaño de la celda dependiendo de la dificultad para que no ocupe toda la pantalla en niveles altos
            tamano_celda = "75px" if filas <= 5 else "55px" if filas == 6 else "45px"
            tamano_fuente = "35px" if filas <= 5 else "25px" if filas == 6 else "20px"

            # Estilo minimalista dependiente de la celda
            fondo = "background-color: var(--secondary-background-color);"
            if celda == 'H': fondo = "background-color: rgba(255, 75, 75, 0.15);"
            elif celda == 'G': fondo = "background-color: rgba(75, 255, 75, 0.15);"
            
            html += f"<td style='width: {tamano_celda}; height: {tamano_celda}; {fondo} text-align: center; font-size: {tamano_fuente}; border-radius: 16px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); transition: transform 0.2s ease;'>{contenido}</td>"
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
        
        st.markdown("##### ⚙️ Configuración")
        
        # Dropdown para los niveles
        nivel_seleccionado = st.selectbox("Dificultad", list(NIVELES.keys()), label_visibility="collapsed")
        mapa_actual = NIVELES[nivel_seleccionado]

        # Selectbox de algoritmo
        algoritmo = st.selectbox("Algoritmo", ["BFS (Garantiza ruta corta)", "DFS (Búsqueda profunda)"], label_visibility="collapsed")
        
        velocidad = 0.50 # Un poco más rápido para los niveles grandes
        
        st.write("")
        ejecutar = st.button("🚀 Iniciar", type="primary", use_container_width=True)
        st.write("")
        
        # Aquí se mostrarán resultados o métricas
        info_placeholder = st.empty()

    with col_mapa:
        # Contenedor para el mapa HTML centrado vertical y horizontalmente
        st.write("") 
        mapa_placeholder = st.empty()
        mapa_placeholder.markdown(renderizar_mapa(mapa_actual, INICIO), unsafe_allow_html=True)

    if ejecutar:
        info_placeholder.info("⏳ Calculando ruta óptima...")
        
        if "BFS" in algoritmo:
            camino, nodos = busqueda_bfs(mapa_actual, INICIO)
        else:
            camino, nodos = busqueda_dfs(mapa_actual, INICIO)

        if camino:
            # Animación paso a paso
            for paso, (px, py) in enumerate(camino):
                mapa_placeholder.markdown(renderizar_mapa(mapa_actual, (px, py)), unsafe_allow_html=True)
                info_placeholder.code(f"🗺️ Paso {paso}/{len(camino)-1}\n🔍 Nodos: {nodos}")
                time.sleep(velocidad)
            
            st.toast(f"¡Meta alcanzada en {len(camino)-1} pasos!", icon="🎉")
            info_placeholder.success(f"**¡Completado!**\n\nPasos: {len(camino)-1} | Evaluación: {nodos} nodos")
        else:
            info_placeholder.error("❌ No se encontró una ruta posible. Hay un bloqueo en el hielo.")