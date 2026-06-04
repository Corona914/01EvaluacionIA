import streamlit as st
import numpy as np

def mostrar_interfaz():
    st.subheader("Búsqueda Local: 8 Reinas")
    st.write("Objetivo: Colocar 8 reinas en un tablero de 8x8 sin que se ataquen entre sí.")
    
    algoritmo = st.selectbox("Algoritmo de búsqueda local:", ["Hill Climbing", "Simulated Annealing"])
    
    if st.button("Generar Estado Inicial Aleatorio"):
        # Representación: el índice es la columna, el valor es la fila
        st.session_state.reinas_estado = np.random.randint(0, 8, 8)
        st.session_state.iteracion = 0
        
    if 'reinas_estado' in st.session_state:
        # Aquí renderizamos el tablero visualmente usando Markdown o HTML simple
        tablero_html = "<table style='border-collapse: collapse;'>"
        for fila in range(8):
            tablero_html += "<tr>"
            for col in range(8):
                color = "#eee" if (fila + col) % 2 == 0 else "#ccc"
                contenido = "👑" if st.session_state.reinas_estado[col] == fila else ""
                tablero_html += f"<td style='width:40px; height:40px; background-color:{color}; text-align:center; font-size:24px;'>{contenido}</td>"
            tablero_html += "</tr>"
        tablero_html += "</table>"
        
        st.markdown(tablero_html, unsafe_allow_html=True)
        
        st.write(f"Iteración actual: {st.session_state.iteracion}")
        
        if st.button("Siguiente Paso de Búsqueda"):
            st.info("Aquí iría la lógica para calcular heurísticas y mover una reina hacia un estado con menos conflictos.")
            # st.session_state.iteracion += 1
            # st.rerun()