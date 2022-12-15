"""Funciones de utilidad para el problema del 8-puzzle."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


HUECO = X = 0


def _iter_matriz(matriz, con_indice=True):
    """
    Recorre `matriz` en row-major order (de arriba a abajo de izquierda a
    derecha) generando tuplas de la forma (fila, columna, valor) si
    ``con_indice == True``, de lo contrario solo genera los valores.
    """
    for i, fila in enumerate(matriz):
        for j, val in enumerate(fila):
            yield (i, j, val) if con_indice else val


def _buscar_elemento(matriz, elemento):
    """Retorna el índice de la primera ocurrencia de `elemento` en `matriz`."""
    """
    # asumiendo `elemento` es único dentro de `matriz`:
    (i,), (j,) = np.where(np.asarray(matriz) == elemento)
    return i, j
    """
    for i, j, val in _iter_matriz(matriz):
        if val == elemento:
            return i, j


_MOVS = (
    # di  dj
    (-1,  0),
    ( 0, -1),
    ( 0,  1),
    ( 1,  0),
)


def _como_mutable(matriz):
    """Retorna una copia mutable de `matriz`."""
    return [list(fila) for fila in matriz]


def _como_hasheable(matriz):
    """Retorna una copia hasheable (y por tanto inmutable) de `matriz`."""
    return tuple(tuple(fila) for fila in matriz)


def gen_estados_alcanzables(estado):
    # print("gen_estados_alcanzables")
    # print(estado)
    """Función generadora de los estados alcanzables a partir de `estado`."""
    i, j = _buscar_elemento(estado, HUECO)
    #M, N = estado.shape  # asumiendo que `estado` es un `np.ndarray`
    """
    pos_huecos = (i, j) + np.asarray(_MOVS)
    # Asumiendo que `estado` es una matriz cuadrada:
    pos_huecos = pos_huecos[  np.all(0 <= pos_huecos, axis=-1)
                            & np.all(pos_huecos < len(estado), axis=-1)]
    """
    pos_huecos = [(i2, j2) for di, dj in _MOVS
                  if (0 <= (i2 := i + di) < len(estado)
                      and 0 <= (j2 := j + dj) < len(estado[i2]))]
    for i2, j2 in pos_huecos:
        estado2 = _como_mutable(estado)
        estado2[i][j], estado2[i2][j2] = estado2[i2][j2], estado2[i][j]
        yield _como_hasheable(estado2)

def es_estado_objetivo(estado, estadoF):
    """
    Determina si `estado` es el estado objetivo, es decir, si corresponde a un
    problema resuelto.
    """
    return np.array_equal(estado, estadoF)


# def dist_manhattan(estado, estadoF):
#     """
#     Retorna la distancia Manhattan entre `estado` y el estado objetivo.
    
#     Se define la distancia Manhattan entre dos estados como la suma de las
#     distancias Manhattan entre las posiciones de las fichas en un estado y sus
#     posiciones correspondientes en el otro estado. Por ejemplo, si la ficha 5
#     se encuentra en la posición (1, 3) en un estado y en la posición (4, 2) en
#     el otro estado, la distancia será de |1 - 4| + |3 - 2| = 4; este proceso se
#     realiza para todas las fichas en `estado`.
#     """
#     dist = 0
#     for i, j, val in _iter_matriz(estado):
#         i2, j2 = _buscar_elemento(estadoF, val)
#         dist += abs(i - i2) + abs(j - j2)
#     return dist


def dist_hamming(estado, estadoF):
    """
    Retorna la distancia Hamming entre `estado` y el estado objetivo.
    
    Se define la distancia Hamming entre dos estados como el número de
    diferencias entre las dos matrices. Las diferencias se cuentan comparando
    las dos matrices elemento por elemento, es decir, si un elemento de una
    matriz no es igual al elemento correspondiente en la otra matriz, cuenta
    como una diferencia.
    """
    return np.not_equal(estado, estadoF).sum()
