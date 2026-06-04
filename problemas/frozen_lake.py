import streamlit as st
import time
from collections import deque

# --- DEFINICIÓN DEL ENTORNO ---
# S: Start, F: Frozen (Seguro), H: Hole (Agujero), G: Goal (Meta)
MAPA_4x4 = [
    ['S', 'F', 'F', 'F'],
    ['F', 'H', 'F', 'H'],
    ['F', 'F', 'F', 'H'],
    ['H', 'F', 'F', 'G']
]

FILAS = len(MAPA_4x4)
COLUMNAS = len(MAPA_4x4[0])
INICIO = (0, 0)

# Diccionario para hacer la interfaz más visual
ICONOS = {
    'S': "🧊", # Inicio
    'F': "❄️", # Hielo seguro
    'H': "🕳️", # Agujero
    'G': "🎁", # Meta
    'A': "🐧"  # Agente (Pingüino)
}

# --- ALGORITMOS DE BÚSQUEDA NO INFORMADA ---

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
    cola = deque([(INICIO, [INICIO])])
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
    html = "<table style='border-collapse: collapse; margin-left: auto; margin-right: auto;'>"
    for f in range(FILAS):
        html += "<tr>"
        for c in range(COLUMNAS):
            celda = MAPA_4x4[f][c]
            contenido = ICONOS['A'] if (f, c) == posicion_agente else ICONOS[celda]
            
            # Colores de fondo según el tipo de celda
            color = "#E0F7FA" if celda in ['S', 'F'] else "#FFEBEE" if celda == 'H' else "#E8F5E9"
            
            html += f"<td style='width:60px; height:60px; background-color:{color}; text-align:center; font-size:30px; border: 1px solid #ccc;'>{contenido}</td>"
        html += "</tr>"
    html += "</table>"
    return html

def mostrar_interfaz():
    st.subheader("Búsqueda No Informada: Frozen Lake")
    st.write("El pingüino 🐧 debe llegar al regalo 🎁 cruzando el hielo ❄️ sin caer en los agujeros 🕳️.")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.write("### Configuración")
        algoritmo = st.radio("Selecciona el algoritmo:", ["BFS (Búsqueda a lo ancho)", "DFS (Búsqueda en profundidad)"])
        velocidad = st.slider("Velocidad de animación (segundos)", 0.1, 1.0, 0.4)
        
        ejecutar = st.button("Ejecutar Búsqueda", type="primary")

    with col2:
        st.write("### Visualización del Entorno")
        # Contenedor vacío para poder actualizar el mapa dinámicamente
        mapa_placeholder = st.empty()
        info_placeholder = st.empty()
        
        # Renderizar mapa inicial
        mapa_placeholder.markdown(renderizar_mapa(INICIO), unsafe_allow_html=True)

    if ejecutar:
        info_placeholder.info("Calculando ruta...")
        
        if "BFS" in algoritmo:
            camino, nodos = busqueda_bfs()
        else:
            camino, nodos = busqueda_dfs()

        if camino:
            # Animación paso a paso
            for paso, (px, py) in enumerate(camino):
                mapa_placeholder.markdown(renderizar_mapa((px, py)), unsafe_allow_html=True)
                info_placeholder.success(f"Paso {paso}/{len(camino)-1} | Nodos explorados en total: {nodos}")
                time.sleep(velocidad)
            
            info_placeholder.success(f"¡Meta alcanzada en {len(camino)-1} pasos! (Algoritmo evaluó {nodos} nodos)")
        else:
            info_placeholder.error("No se encontró una ruta posible.")