import math
import random
from problemas.algoritmos.hill_climbing import evaluar

def obtener_vecino_aleatorio(estado_actual):
    """Genera un vecino aleatorio moviendo una sola reina a una casilla diferente en su columna."""
    n = len(estado_actual)
    vecino = estado_actual.copy()
    col = random.randint(0, n - 1)
    fila = random.randint(0, n - 1)
    
    # Asegurarnos de que realmente se mueva
    while fila == estado_actual[col]:
        fila = random.randint(0, n - 1)
        
    vecino[col] = fila
    return vecino

def paso_simulated_annealing(estado_actual, temperatura, factor_enfriamiento=0.95):
    """
    Ejecuta una iteración (paso) de recocido simulado.
    Retorna el estado resultante y la nueva temperatura.
    """
    if temperatura <= 0.01:
        return estado_actual, temperatura  # El sistema se ha "congelado"

    vecino = obtener_vecino_aleatorio(estado_actual)
    
    energia_actual = evaluar(estado_actual)
    energia_vecino = evaluar(vecino)
    
    delta_e = energia_vecino - energia_actual
    
    # Criterio de Aceptación Metropolis
    if delta_e < 0:
        # Si mejora, se acepta
        estado_actual = vecino
    else:
        # Si empeora, se acepta con cierta probabilidad
        prob_aceptacion = math.exp(-delta_e / temperatura)
        if random.random() < prob_aceptacion:
            estado_actual = vecino
            
    # Enfriamiento
    nueva_temperatura = temperatura * factor_enfriamiento
    
    return estado_actual, nueva_temperatura
