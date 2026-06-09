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
