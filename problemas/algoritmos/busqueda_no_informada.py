from collections import deque

def obtener_vecinos(x, y, filas, columnas):
    """Devuelve las posiciones adyacentes válidas (Derecha, Abajo, Izquierda, Arriba)."""
    movimientos = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    vecinos = []
    for dx, dy in movimientos:
        nx, ny = x + dx, y + dy
        if 0 <= nx < filas and 0 <= ny < columnas:
            vecinos.append((nx, ny))
    return vecinos

def busqueda_bfs(mapa, inicio):
    """Búsqueda a lo ancho: Explora nivel por nivel (Garantiza ruta más corta)."""
    filas = len(mapa)
    columnas = len(mapa[0])
    cola = deque([(inicio, [inicio])]) #fifo
    visitados = set([inicio])
    nodos_explorados = 0

    while cola:
        (x, y), camino = cola.popleft()
        nodos_explorados += 1

        if mapa[x][y] == 'G':
            return camino, nodos_explorados

        for nx, ny in obtener_vecinos(x, y, filas, columnas):
            if (nx, ny) not in visitados and mapa[nx][ny] != 'H':
                visitados.add((nx, ny))
                cola.append(((nx, ny), camino + [(nx, ny)]))
                
    return None, nodos_explorados

def busqueda_dfs(mapa, inicio):
    """Búsqueda en profundidad: Explora una rama hasta el fondo antes de retroceder."""
    filas = len(mapa)
    columnas = len(mapa[0])
    pila = [(inicio, [inicio])]
    visitados = set([inicio])
    nodos_explorados = 0

    while pila:
        (x, y), camino = pila.pop() # LIFO (Last In, First Out)
        nodos_explorados += 1

        if mapa[x][y] == 'G':
            return camino, nodos_explorados

        for nx, ny in obtener_vecinos(x, y, filas, columnas):
            if (nx, ny) not in visitados and mapa[nx][ny] != 'H':
                visitados.add((nx, ny))
                pila.append(((nx, ny), camino + [(nx, ny)]))
                
    return None, nodos_explorados