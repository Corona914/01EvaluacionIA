import streamlit as st
import time
from problemas.algoritmos.AEstrella import busqueda_a_estrella, parsear_mapa

# --- DEFINICIÓN DEL ENTORNO ---
# #: Pared, ' ': Espacio, T: Objetivo (Target), B: Caja (Box), W: Trabajador (Worker)

# Diccionario con 4 niveles de dificultad (Asegúrate de que todas las filas tengan el mismo ancho en cada nivel)
NIVELES = {
    "Nivel 1 (Fácil)": [
        "######",
        "#T B #",
        "# W  #",
        "######"
    ],
    "Nivel 2 (Intermedio)": [
        "########",
        "#T     #",
        "#      #",
        "## B W #",
        "#  B T #",
        "#      #",
        "########"
    ],
    "Nivel 3 (Difícil)": [
        "#######",
        "#T    #",
        "#  BB #",
        "#T W  #",
        "#######"
    ],
    "Nivel 4 (Experto)": [
        "#########",
        "#       #",
        "# T B#  #",
        "# T   W #",
        "#  #B   #",
        "#       #",
        "#########"
    ]
}

ICONOS = {
    '#': "🧱",
    ' ': "⬛",
    'T': "🎯",
    'B': "📦",
    'W': "👷",
    'X': "✅" # Caja sobre el objetivo
}

# --- INTERFAZ STREAMLIT ---

def renderizar_mapa(ancho, alto, paredes, objetivos, trabajador, cajas):
    """Genera el HTML del mapa combinando las posiciones actuales."""
    html = "<div style='display:flex; justify-content:center;'><table style='border-collapse: separate; border-spacing: 6px; margin: 0 auto;'>"
    for y in range(alto):
        html += "<tr>"
        for x in range(ancho):
            pos = (x, y)
            if pos in paredes:
                contenido = ICONOS['#']
                color = "#424242"
            elif pos in cajas and pos in objetivos:
                contenido = ICONOS['X']
                color = "#81C784"
            elif pos in cajas:
                contenido = ICONOS['B']
                color = "#FFB74D"
            elif pos == trabajador:
                contenido = ICONOS['W']
                color = "#64B5F6"
            elif pos in objetivos:
                contenido = ICONOS['T']
                color = "rgba(120, 120, 120, 0.12)"
            else:
                contenido = ICONOS[' ']
                color = "rgba(255, 255, 255, 0.04)"
                
            html += f"<td style='width:52px; height:52px; background-color:{color}; text-align:center; font-size:26px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); box-shadow: 0 2px 8px rgba(0,0,0,0.05);'>{contenido}</td>"
        html += "</tr>"
    html += "</table></div>"
    return html

def mostrar_interfaz():
    st.title("🧩 Sokoban")
    st.caption("A* guía al trabajador para empujar las cajas hasta los objetivos con la menor cantidad de movimientos.")
    st.markdown("---")

    col1, col2 = st.columns([1, 1.6])

    with col1:
        st.markdown("##### Configuración")
        
        # Selector de nivel de dificultad
        nivel_seleccionado = st.selectbox(
            "Selecciona la dificultad:", 
            list(NIVELES.keys())
        )
        mapa_actual = NIVELES[nivel_seleccionado]
        
        st.caption("Algoritmo: A*")
        st.caption("Heurística: Distancia Manhattan")
        velocidad = 0.50
        ejecutar = st.button("Resolver nivel", type="primary", use_container_width=True)

    # El análisis del mapa ocurre DESPUÉS de que se selecciona el nivel en el dropdown
    paredes, objetivos, inicio_trabajador, inicio_cajas = parsear_mapa(mapa_actual)
    alto = len(mapa_actual)
    ancho = len(mapa_actual[0])

    with col2:
        st.markdown("##### Visualización")
        mapa_placeholder = st.empty()
        info_placeholder = st.empty()
        
        mapa_placeholder.markdown(renderizar_mapa(ancho, alto, paredes, objetivos, inicio_trabajador, inicio_cajas), unsafe_allow_html=True)

    if ejecutar:
        info_placeholder.info(f"Ejecutando algoritmo A* para el {nivel_seleccionado}...")
        
        camino_w, camino_c, nodos = busqueda_a_estrella(paredes, objetivos, inicio_trabajador, inicio_cajas)

        if camino_w:
            for paso in range(len(camino_w)):
                trabajador_actual = camino_w[paso]
                cajas_actuales = camino_c[paso]
                
                mapa_placeholder.markdown(
                    renderizar_mapa(ancho, alto, paredes, objetivos, trabajador_actual, cajas_actuales), 
                    unsafe_allow_html=True
                )
                info_placeholder.success(f"Paso {paso}/{len(camino_w)-1} | Nodos evaluados en total por A*: {nodos}")
                time.sleep(velocidad)
            
            info_placeholder.success(f"¡Nivel resuelto óptimamente en {len(camino_w)-1} movimientos!")
        else:
            info_placeholder.error("No se encontró una solución posible para este nivel.")