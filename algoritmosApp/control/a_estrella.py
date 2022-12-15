"""Resolver un 8-puzzle usando búsqueda A*."""

from bisect import insort
from collections import deque
from math import isinf

from algoritmosApp.utils.indicadores_progreso import ContadorPasos
from algoritmosApp.utils.nodos import NodoConCostoCombinado as Nodo, reconstruir_ruta


def buscar_con_a_estrella(estado0, estadoF, gen_estados_alcanzables, heuristica):
    """Retorna la ruta para resolver el problema, o `None` si no se encontró
    una solución.

    :param `estado0`: estado inicial
    :param `gen_estados_alcanzables` función que recibe un estado y genera los
        estados alcanzables a partir de este
    :param heuristica: función que recibe un estado y estima qué tan cerca está
        del estado objetivo; debe retornar 0 si el estado es el estado objetivo
    """
    conteo = 0
    print("ESTADOS ALCANZABLES:")
    # contador_pasos = ContadorPasos()
    if isinf(dist := heuristica(estado0, estadoF)):
        return None  # no resuelto
    frontera = deque([Nodo(estado=estado0, padre=None, costo_actual=0,
                           dist=dist, costo_combinado=0+dist)])
    considerados = {estado0}  # estados en la frontera o ya visitados
    while frontera:
        conteo = conteo + 1
        print(conteo)
        # next(contador_pasos)
        nodo = frontera.popleft()
        if nodo.dist == 0:
            return reconstruir_ruta(nodo), conteo
        hijos = set(gen_estados_alcanzables(nodo.estado)) - considerados
        for hijo in hijos:
            if not isinf(dist := heuristica(hijo, estadoF)):
                costo_hijo = nodo.costo_actual + 1
                insort(frontera,
                       Nodo(estado=hijo, padre=nodo, costo_actual=costo_hijo,
                            dist=dist, costo_combinado=costo_hijo+dist))
                considerados.add(hijo)
    return None  # no resuelto

