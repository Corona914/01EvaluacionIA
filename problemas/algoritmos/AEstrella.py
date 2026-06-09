import heapq


def parsear_mapa(mapa):
    """Separa los elementos estáticos (paredes, objetivos) de los dinámicos (cajas, trabajador)."""
    paredes = set()
    objetivos = set()
    cajas = []
    trabajador = None

    for y, fila in enumerate(mapa):
        for x, char in enumerate(fila):
            if char == '#':
                paredes.add((x, y))
            elif char == 'T':
                objetivos.add((x, y))
            elif char == 'B':
                cajas.append((x, y))
            elif char == 'W':
                trabajador = (x, y)

    return paredes, objetivos, trabajador, tuple(cajas)


def distancia_manhattan(p1, p2):
    """Heurística: Distancia en cuadrícula entre dos puntos."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def heuristica(cajas, objetivos):
    """Calcula la distancia de cada caja a su objetivo más cercano."""
    total = 0
    for caja in cajas:
        if objetivos:
            total += min(distancia_manhattan(caja, objetivo) for objetivo in objetivos)
    return total


def busqueda_a_estrella(paredes, objetivos, inicio_trabajador, inicio_cajas):
    """Algoritmo A* para resolver Sokoban."""
    cola = []
    h_inicial = heuristica(inicio_cajas, objetivos)
    heapq.heappush(
        cola,
        (
            h_inicial,
            0,
            inicio_trabajador,
            inicio_cajas,
            [inicio_trabajador],
            [inicio_cajas],
        ),
    )

    visitados = {(inicio_trabajador, inicio_cajas)}
    nodos_explorados = 0
    movimientos = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    while cola:
        _, g, trabajador, cajas, camino_w, camino_c = heapq.heappop(cola)
        nodos_explorados += 1

        if set(cajas) == objetivos:
            return camino_w, camino_c, nodos_explorados

        wx, wy = trabajador

        for dx, dy in movimientos:
            nx, ny = wx + dx, wy + dy

            if (nx, ny) in paredes:
                continue

            nuevas_cajas = list(cajas)
            movimiento_valido = True

            if (nx, ny) in nuevas_cajas:
                idx_caja = nuevas_cajas.index((nx, ny))
                bx, by = nx + dx, ny + dy

                if (bx, by) in paredes or (bx, by) in nuevas_cajas:
                    movimiento_valido = False
                else:
                    nuevas_cajas[idx_caja] = (bx, by)

            if not movimiento_valido:
                continue

            nuevas_cajas_tupla = tuple(nuevas_cajas)
            estado = ((nx, ny), nuevas_cajas_tupla)

            if estado in visitados:
                continue

            visitados.add(estado)
            nuevo_g = g + 1
            nuevo_f = nuevo_g + heuristica(nuevas_cajas_tupla, objetivos)

            heapq.heappush(
                cola,
                (
                    nuevo_f,
                    nuevo_g,
                    (nx, ny),
                    nuevas_cajas_tupla,
                    camino_w + [(nx, ny)],
                    camino_c + [nuevas_cajas_tupla],
                ),
            )

    return None, None, nodos_explorados