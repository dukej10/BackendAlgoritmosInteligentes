"""Funciones de utilidad para el problema del 8-puzzle."""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


HUECO = X = 0


def _iter_matriz(matriz, con_indice=True):
    """
    Recorre `matriz` de arriba a abajo de izquierda a
    derecha generando tuplas,sino devuele el valor
    """
    for i, fila in enumerate(matriz):
        for j, val in enumerate(fila):
            yield (i, j, val) if con_indice else val


def _buscar_elemento(matriz, elemento):
    """Retorna el índice de la primera ocurrencia de `elemento` en `matriz`."""
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
    """Encarada de obtener los estados alcanzable a partir del estado que recibe."""
    i, j = _buscar_elemento(estado, HUECO)
    pos_huecos = [(i2, j2) for di, dj in _MOVS
                  if (0 <= (i2 := i + di) < len(estado)
                      and 0 <= (j2 := j + dj) < len(estado[i2]))]
    for i2, j2 in pos_huecos:
        estado2 = _como_mutable(estado)
        estado2[i][j], estado2[i2][j2] = estado2[i2][j2], estado2[i][j]
        yield _como_hasheable(estado2)

def es_estado_objetivo(estado, estadoF):
    """
    Verifica que el estado que recibe corresponda al estado objetivo
    """
    return np.array_equal(estado, estadoF)


def dist_hamming(estado, estadoF):
    """
    Retorna la distancia Hamming entre `estado` y el estado objetivo.
    cuentan comparando las dos matrices elemento por elemento y contando la cantidad
    de diferencias
    """
    return np.not_equal(estado, estadoF).sum()
