"""Resolver un 8-puzzle usando búsqueda voraz."""

from bisect import insort
from collections import deque

from algoritmosApp.utils.indicadores_progreso import ContadorPasos
from algoritmosApp.nodo import NodoConHeuristica as Nodo, reconstruir_ruta


def buscar_primero(estado0, gen_estados_alcanzables, estadoF,heuristica):
    """Retorna la ruta para resolver el problema, o `None` si no se encontró
    una solución.

    :param `estado0`: estado inicial
    :param `gen_estados_alcanzables` función que recibe un estado y genera los
        estados alcanzables a partir de este
    :param heuristica: función que recibe un estado y estima qué tan cerca está
        del estado objetivo; debe retornar 0 si el estado es el estado objetivo
    """
    lista = []
    conteo = 0
    frontera = deque([Nodo(estado=estado0, padre=None,
                           dist=heuristica(estado0, estadoF))])
    considerados = {estado0} 
    while frontera:
        nodo = frontera.popleft()
        if nodo not in lista:
            lista.append(nodo)
            conteo = conteo + 1
        if nodo.dist == 0:
            return reconstruir_ruta(nodo), conteo
        hijos = set(gen_estados_alcanzables(nodo.estado)) - considerados
        for hijo in hijos:
            insort(frontera, Nodo(estado=hijo, padre=nodo,
                                  dist=heuristica(hijo, estadoF)))
            considerados.add(hijo)
    return None  # no resuelto


