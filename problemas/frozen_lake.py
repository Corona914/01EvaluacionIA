import streamlit as st
import time
from collections import deque


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


def obtener_vecinos(x, y):
    """Devuelve las posiciones adyacentes válidas (Derecha, Abajo, Izquierda, Arriba)."""
    movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    vecinos = []
    for dx, dy in movimientos:
        nx, ny = x + dx, y + dy
        if 0 <= nx < FILAS and 0 <= ny < COLUMNAS:
            vecinos.append((nx, ny))
    return vecinos

def busqueda_bfs():
    """Búsqueda a lo ancho: Explora nivel por nivel (Garantiza ruta más corta)."""
    cola = deque([(INICIO, [INICIO])]) #fifo
    visitados = set([INICIO])
    nodos_explorados = 0

    while cola:
        (x, y), camino = cola.popleft()
        nodos_explorados += 1

        if MAPA_4x4[x][y] == 'G':
            return camino, nodos_explorados

        for nx, ny in obtener_vecinos(x, y):
            if (nx, ny) not in visitados and MAPA_4x4[nx][ny] != 'H':
                visitados.add((nx, ny))
                cola.append(((nx, ny), camino + [(nx, ny)]))
                
    return None, nodos_explorados

def busqueda_dfs():
    """Búsqueda en profundidad: Explora una rama hasta el fondo antes de retroceder."""
    pila = [(INICIO, [INICIO])]
    visitados = set([INICIO])
    nodos_explorados = 0

    while pila:
        (x, y), camino = pila.pop() # LIFO (Last In, First Out)
        nodos_explorados += 1

        if MAPA_4x4[x][y] == 'G':
            return camino, nodos_explorados

        for nx, ny in obtener_vecinos(x, y):
            if (nx, ny) not in visitados and MAPA_4x4[nx][ny] != 'H':
                visitados.add((nx, ny))
                pila.append(((nx, ny), camino + [(nx, ny)]))
                
    return None, nodos_explorados

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
        
        st.markdown("##### ⏱️ Velocidad")
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
            camino, nodos = busqueda_bfs()
        else:
            camino, nodos = busqueda_dfs()

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