"""Resolver un 8-puzzle usando búsqueda en anchura con cortocircuito, es decir,
verifica si alguno de los hijos de un estado es el estado objetivo antes de
expandirlos.
"""

from collections import deque

from algoritmosApp.utils.indicadores_progreso import ContadorPasos
from algoritmosApp.utils.nodos import Nodo, reconstruir_ruta


def buscar_en_anchura(estado0, gen_estados_alcanzables, es_estado_objetivo):
    """Retorna la ruta para resolver el problema, o `None` si no se encontró
    una solución.

    :param `estado0`: estado inicial
    :param `gen_estados_alcanzables` función que recibe un estado y genera los
        estados alcanzables a partir de este
    :param `es_estado_objetivo`: función que recibe un estado e indica si es el
        estado objetivo
    """
    contador_pasos = ContadorPasos()
    nodo = Nodo(estado0, padre=None)
    if es_estado_objetivo(estado0):
        return reconstruir_ruta(nodo)
    frontera = deque([nodo])  # estados por visitar
    considerados = {estado0}  # estados en la frontera o ya visitados
    while frontera:
        next(contador_pasos)
        nodo = frontera.popleft()
        #hijos = set(gen_estados_alcanzables(nodo.estado)) - considerados
        # Si se desea preservar el orden de los hijos generados:
        hijos = [hijo for hijo in gen_estados_alcanzables(nodo.estado)
                 if hijo not in considerados]
        for hijo in hijos:
            nodo_hijo = Nodo(estado=hijo, padre=nodo)
            if es_estado_objetivo(hijo):
                return reconstruir_ruta(nodo_hijo)
            frontera.append(nodo_hijo)
            considerados.add(hijo)
    return None  # no resuelto


# if __name__ == "__main__":
#     import utils.eight_puzzle as ep

#     X = ep.HUECO
#     estado0 = (
#         (5, 1, 2),
#         (X, 7, 3),
#         (6, 4, 8),
#     )
#     ep.graficar_estado(estado0)
#     ruta = buscar_en_anchura(estado0, ep.gen_estados_alcanzables,
#                              ep.es_estado_objetivo)
#     print(f'Solución de {len(ruta)} pasos')
#     ep.graficar_ruta(ruta)
