import streamlit as st
import numpy as np
from problemas.algoritmos.hill_climbing import evaluar, obtener_mejor_vecino

# --- INTERFAZ STREAMLIT ---
def renderizar_tablero(estado):
    """Dibuja un tablero de ajedrez minimalista."""
    # Contenedor flex para centrar y aplicar bordes redondeados al tablero
    tablero_html = "<div style='display: flex; justify-content: center;'><table style='border-collapse: collapse; border-spacing: 0; box-shadow: 0 4px 15px rgba(0,0,0,0.1); border-radius: 12px; overflow: hidden;'>"
    for fila in range(8):
        tablero_html += "<tr>"
        for col in range(8):
            # Celdas minimalistas
            es_blanca = (fila + col) % 2 == 0
            color_fondo = "rgba(255, 255, 255, 0.05)" if es_blanca else "rgba(128, 128, 128, 0.15)"
            contenido = "👑" if estado[col] == fila else ""
            
            tablero_html += f"<td style='width: 55px; height: 55px; background-color: {color_fondo}; text-align: center; font-size: 30px; transition: transform 0.2s;'>{contenido}</td>"
        tablero_html += "</tr>"
    tablero_html += "</table></div>"
    return tablero_html

def mostrar_interfaz():
    st.title("👑 8 Reinas")
    st.markdown("---")
    
    col_info, col_tablero = st.columns([1, 2])
    
    with col_info:
        st.markdown(
            "Posiciona 8 reinas en un tablero de **8x8**<br>"
            "sin que se ataquen entre sí.",
            unsafe_allow_html=True
        )
        st.write("")
        
        st.markdown("##### ⚙️ Algoritmo")
        algoritmo = st.selectbox("Alg", ["Hill Climbing", "Simulated Annealing"], label_visibility="collapsed")
        
        st.write("")
        if st.button("🎲 Tablero Aleatorio", type="primary", use_container_width=True):
            st.session_state.reinas_estado = np.random.randint(0, 8, 8)
            st.session_state.iteracion = 0
            st.session_state.optimo_local = False
            
        st.write("")
        metrics_placeholder = st.empty()
        
    with col_tablero:
        st.write("")
        if 'reinas_estado' in st.session_state:
            st.markdown(renderizar_tablero(st.session_state.reinas_estado), unsafe_allow_html=True)
            
            st.write("")
            col_btn1, col_btn2, col_btn3 = st.columns([1,2,1])
            with col_btn2:
                h_actual = evaluar(st.session_state.reinas_estado)
                
                # Acciones minimalistas
                if h_actual == 0:
                    st.toast("¡Solución óptima encontrada!", icon="🎉")
                elif st.session_state.get('optimo_local', False):
                    st.toast("Óptimo local alcanzado. Intenta con otro tablero.", icon="🔒")
                else:
                    if st.button("🚀 Siguiente Paso", use_container_width=True):
                        if algoritmo == "Hill Climbing":
                            mejor_estado, mejor_h = obtener_mejor_vecino(st.session_state.reinas_estado)
                            
                            if mejor_h >= h_actual:
                                st.session_state.optimo_local = True
                            else:
                                st.session_state.reinas_estado = mejor_estado
                                st.session_state.iteracion += 1
                                
                            st.rerun()

            # Resumen visual en la columna izquierda
            with metrics_placeholder.container():
                st.code(f"🔄 Iteración: {st.session_state.iteracion}\n⚔️ Ataques: {h_actual}")
                
                # Feedback de estado estético
                if h_actual == 0:
                    st.success("**¡Completado!**\n\n0 Ataques detectados.")
                elif st.session_state.get('optimo_local', False):
                    st.error("**Atascado**\n\nNingún movimiento mejora el estado.")