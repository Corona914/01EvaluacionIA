def evaluar(estado):
    """Calcula cuántos pares de reinas se están atacando (conflictos)."""
    conflictos = 0
    n = len(estado)
    for i in range(n):
        for j in range(i + 1, n):
            if estado[i] == estado[j]: # Misma fila
                conflictos += 1
            elif abs(estado[i] - estado[j]) == abs(i - j): # Misma diagonal
                conflictos += 1
    return conflictos

def obtener_mejor_vecino(estado_actual):
    """Obtiene todos los vecinos y retorna el que tiene menos conflictos, ajustado al código original."""
    n = len(estado_actual)
    vecinos = []
    
    # Generar vecinos
    for columna in range(n):
        for fila in range(n):
            if fila != estado_actual[columna]:
                vecino = estado_actual.copy()
                vecino[columna] = fila
                vecinos.append(vecino)

    mejor_vecino = None
    mejores_conflictos = float('inf')
    
    # Buscar el vecino con menos conflictos
    for vecino in vecinos:
        conflictos_vecino = evaluar(vecino)
        if conflictos_vecino < mejores_conflictos:
            mejores_conflictos = conflictos_vecino
            mejor_vecino = vecino
            
    return mejor_vecino, mejores_conflictos