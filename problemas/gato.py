import streamlit as st
import random
from problemas.algoritmos.minimax import verificar_ganador, mejor_movimiento

# --- INTERFAZ STREAMLIT ---
@st.dialog("¡Fin del Juego!")
def popup_resultado(ganador):
    if ganador == "Empate":
        st.info("¡Es un reñido empate! 🤝")
    elif ganador == "X":
        st.success("¡Increíble! Has derrotado a la IA. 🎉")
        st.balloons()
    else:
        st.error("¡Has perdido! La IA ha demostrado ser superior. 🤖")

    if st.button("Volver a Jugar", type="primary", use_container_width=True):
        st.session_state.tablero_gato = [" "] * 9
        st.session_state.ganador_gato = None
        st.rerun()

def mostrar_interfaz():
    st.title("🎮 Gato vs IA")
    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(
            "Enfréntate a la IA eligiendo tu nivel de desafío.\n\n"
            "Tú juegas como **❌** y tienes el primer turno."
        )
        
        st.markdown("##### ⚙️ Dificultad")
        dificultad = st.selectbox(
            "Nivel", 
            [
                "Nivel 1: Fácil (Aleatorio)", 
                "Nivel 2: Intermedio (Equilibrado)", 
                "Nivel 3: Difícil (Minimax Invencible)"
            ], 
            label_visibility="collapsed"
        )
        
    with col2:
        st.write("")
        st.write("")
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
                # Obtener lista de casillas vacías
                vacios = [i for i, x in enumerate(st.session_state.tablero_gato) if x == " "]
                mov = None
                
                if vacios:
                    if "Fácil" in dificultad:
                        # Nivel Fácil: Movimiento 100% aleatorio
                        mov = random.choice(vacios)
                    
                    elif "Intermedio" in dificultad:
                        # Nivel Intermedio: 50% de probabilidad de usar Minimax, 50% aleatorio
                        if random.random() < 0.5:
                            mov = mejor_movimiento(st.session_state.tablero_gato)
                        else:
                            mov = random.choice(vacios)
                    
                    else:
                        # Nivel Difícil: 100% Minimax
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