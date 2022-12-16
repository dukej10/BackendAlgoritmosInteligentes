"""Resolver un 8-puzzle usando búsqueda en anchura con cortocircuito, es decir,
verifica si alguno de los hijos de un estado es el estado objetivo antes de
expandirlos.
"""

from collections import deque

from algoritmosApp.utils.indicadores_progreso import ContadorPasos
from algoritmosApp.nodo import Nodo, reconstruir_ruta


def buscar_en_anchura(estado0, gen_estados_alcanzables, es_estado_objetivo, estadoF):
    """Retorna la ruta para resolver el problema, o `None` si no se encontró
    una solución.

    :param `estado0`: estado inicial
    :param `gen_estados_alcanzables` función que recibe un estado y genera los
        estados alcanzables a partir de este
    :param `es_estado_objetivo`: función que recibe un estado e indica si es el
        estado objetivo
    """
    conteo = 0
    lista = []
    nodo = Nodo(estado0, padre=None)
    if es_estado_objetivo(estado0, estadoF):
        return reconstruir_ruta(nodo)
    frontera = deque([nodo])  # estados por visitar
    considerados = {estado0}  # estados en la frontera o ya visitados
    while frontera:
        nodo = frontera.popleft()
        if nodo not in lista:
            lista.append(nodo)
            conteo = conteo + 1
        # Si se desea preservar el orden de los hijos generados:
        hijos = [hijo for hijo in gen_estados_alcanzables(nodo.estado)
                 if hijo not in considerados]
        for hijo in hijos:
            nodo_hijo = Nodo(estado=hijo, padre=nodo)
            if es_estado_objetivo(hijo, estadoF):
                return reconstruir_ruta(nodo_hijo), conteo
            frontera.append(nodo_hijo)
            considerados.add(hijo)
    return None  # no resuelto

