"""Estructuras de datos y funciones útiles para resolver el problema del
cuadrado mágico.
"""

import numpy as np


ESTADO0 = (
    (0, 0, 0),
    (0, 0, 0),
    (0, 0, 0),
)


def gen_sucesores(estado):
    estado = np.asarray(estado)
    m, n = estado.shape
    nums = [num for num in range(1, m * n + 1) if num not in estado.ravel()]
    if not nums:
        return []
    i, j = np.argwhere(estado == 0)[0]
    for num in nums:
        estado[i, j] = num
        yield tuple(tuple(fila) for fila in estado)


def _hallar_sumas(cuadrado):
    suma_diag1 = np.trace(cuadrado)
    suma_diag2 = np.trace(np.fliplr(cuadrado))
    sumas_cols = cuadrado.sum(axis=0)
    sumas_filas = cuadrado.sum(axis=1)
    return np.concatenate(((suma_diag1, suma_diag2), sumas_cols, sumas_filas))


def test_objetivo(estado):
    estado = np.asarray(estado)
    if np.count_nonzero(estado == 0) > 0:
        return False
    sumas = _hallar_sumas(estado)
    return all(suma == sumas[0] for suma in sumas)


def heuristica(estado, c=256):
    estado = np.asarray(estado)
    m, n = estado.shape
    objetivo = n * (n ** 2 + 1) / 2  # asumiendo que m = n
    sumas = _hallar_sumas(estado)
    if any(suma > objetivo for suma in sumas):
        return float('inf')
    return np.sum(15 - sumas) +  c * (estado[0, 0] != 8)
