"""Estructuras de datos y funciones útiles para los algoritmos."""

from collections import deque, namedtuple


Nodo = namedtuple('Nodo', ['estado', 'padre'])
NodoConHeuristica = namedtuple('Nodo', ['dist', 'estado', 'padre'])
NodoConCostoCombinado = namedtuple(
    'Nodo', ['costo_combinado', 'costo_actual', 'dist', 'estado', 'padre'])


def reconstruir_ruta(nodo):
    ruta = deque([nodo.estado])
    while (nodo := nodo.padre) is not None:
        ruta.appendleft(nodo.estado)
    return ruta
