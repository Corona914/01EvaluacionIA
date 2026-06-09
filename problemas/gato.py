import streamlit as st
import math

def verificar_ganador(tablero):
    lineas = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Filas
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Columnas
        [0, 4, 8], [2, 4, 6]             # Diagonales
    ]
    for linea in lineas:
        if tablero[linea[0]] == tablero[linea[1]] == tablero[linea[2]] and tablero[linea[0]] != " ":
            return tablero[linea[0]]
    if " " not in tablero:
        return "Empate"
    return None

def minimax(tablero, profundidad, es_maximizador):
    ganador = verificar_ganador(tablero)
    if ganador == "O": return 10 - profundidad #IA MAX
    if ganador == "X": return profundidad - 10
    if ganador == "Empate": return 0

    if es_maximizador:
        mejor_puntaje = -math.inf
        for i in range(9):
            if tablero[i] == " ":
                tablero[i] = "O"
                puntaje = minimax(tablero, profundidad + 1, False)
                tablero[i] = " " #backtracking
                mejor_puntaje = max(puntaje, mejor_puntaje)
        return mejor_puntaje
    else:
        mejor_puntaje = math.inf
        for i in range(9):
            if tablero[i] == " ":
                tablero[i] = "X"
                puntaje = minimax(tablero, profundidad + 1, True)
                tablero[i] = " "
                mejor_puntaje = min(puntaje, mejor_puntaje)
        return mejor_puntaje

def mejor_movimiento(tablero):
    mejor_puntaje = -math.inf
    movimiento = None
    for i in range(9):
        if tablero[i] == " ":
            tablero[i] = "O" 
            puntaje = minimax(tablero, 0, False)
            tablero[i] = " "
            if puntaje > mejor_puntaje:
                mejor_puntaje = puntaje
                movimiento = i
    return movimiento

# --- INTERFAZ STREAMLIT ---
@st.dialog("¡Fin del Juego!")
def popup_resultado(ganador):
    if ganador == "Empate":
        st.info("¡Es un reñido empate! ")
    elif ganador == "X":
        st.success("¡Increíble! Has derrotado a la IA. 🎉")
        st.balloons()
    else:
        st.error("¡Has perdido! La IA ha demostrado ser superior.")

    if st.button("Volver a Jugar", type="primary", use_container_width=True):
        st.session_state.tablero_gato = [" "] * 9
        st.session_state.ganador_gato = None
        st.rerun()

def mostrar_interfaz():
    st.title("🎮 Gato vs IA (Minimax)")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            "Enfréntate a la IA utilizando el algoritmo **Minimax**.\n\n"
            "Tú juegas como **❌** y tienes el primer turno."
        )
    with col2:
        if st.button("🔄 Reiniciar Partida", use_container_width=True):
            st.session_state.tablero_gato = [" "] * 9
            st.session_state.ganador_gato = None
            st.rerun()

    # Estilos CSS modernos para los botones del gato
    st.markdown("""
        <style>
        div[data-testid="stButton"] button {
            height: 100px;
            font-size: 40px !important;
            font-weight: bold;
            border-radius: 15px;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        div[data-testid="stButton"] button:hover {
            transform: scale(1.05);
            box-shadow: 0px 4px 15px rgba(0,0,0,0.2);
        }
        </style>
    """, unsafe_allow_html=True)

    if 'tablero_gato' not in st.session_state:
        st.session_state.tablero_gato = [" "] * 9
        st.session_state.ganador_gato = None

    def jugar(idx):
        if st.session_state.tablero_gato[idx] == " " and not st.session_state.ganador_gato:
            # Turno del jugador
            st.session_state.tablero_gato[idx] = "X"
            st.session_state.ganador_gato = verificar_ganador(st.session_state.tablero_gato)
            
            # Turno de la IA
            if not st.session_state.ganador_gato:
                mov = mejor_movimiento(st.session_state.tablero_gato)
                if mov is not None:
                    st.session_state.tablero_gato[mov] = "O"
                    st.session_state.ganador_gato = verificar_ganador(st.session_state.tablero_gato)

    st.write("")
    
    # Dibujar tablero (centrado en la pantalla)
    col_izq, col_centro, col_der = st.columns([1, 2, 1])
    
    with col_centro:
        for fila in range(3):
            cols = st.columns(3)
            for col in range(3):
                idx = fila * 3 + col
                with cols[col]:
                    valor = st.session_state.tablero_gato[idx]
                    simbolo = "❌" if valor == "X" else "🔵" if valor == "O" else " "
                    st.button(
                        simbolo, 
                        key=f"btn_{idx}", 
                        on_click=jugar, 
                        args=(idx,),
                        use_container_width=True
                    )

    if st.session_state.ganador_gato:
        popup_resultado(st.session_state.ganador_gato)
