"""Resolver un 8-puzzle usando búsqueda en profundidad iterativa."""

import sys
from collections import deque

from algoritmosApp.utils.indicadores_progreso import ContadorPasos


def _buscar_limite_profundidad(
        estado0, gen_estados_alcanzables, es_estado_objetivo, max_profundidad,estadoF,
        contador_pasos=None):
    """Retorna la maxima profundiad.

    :param `estado0`: estado inicial
    :param `gen_estados_alcanzables` función que recibe un estado y genera los
        estados alcanzables a partir de este
    :param `es_estado_objetivo`: función que recibe un estado e indica si es el
        estado objetivo
    :param `max_profundidad`: profundidad máxima de búsqueda; no se sigue
        buscando soluciones de más de `max_profundidad` pasos
    """
    frontera = deque([estado0]) 
    print(frontera) # estados por visitar
    ruta = []
    pendientes = [1]  # `pendientes[i]` es el número de hijos de `ruta[i-1]`
                      # pendientes por visitar
    print('Buscando solución...')
    for pasos in contador_pasos or ContadorPasos():
        estado = frontera.pop()
        
        ruta.append(estado)
        pendientes[-1] -= 1

        if ((profundidad := len(ruta) - 1) < max_profundidad and (hijos := [
                hijo for hijo in gen_estados_alcanzables(estado)
                if hijo not in ruta and hijo not in frontera] )):
           # print("PROFUNDIDAD: ", profundidad)
            if any(es_estado_objetivo(objetivo := hijo, estadoF) for hijo in hijos):
                ruta.append(objetivo)
                return max_profundidad
            frontera.extend(hijos)
            pendientes.append(len(hijos))
        else:
            # Se retiran los estados cuyos hijos ya fueron visitados:
            pendientes.append(0)
            while (pendientes[-1] == 0):
                ruta.pop()
                pendientes.pop()
                if not ruta:
                    return None  # no resuelto
    
def _buscar_profundidad(
        estado0, gen_estados_alcanzables, es_estado_objetivo, max_profundidad,
        estadoF,
        contador_pasos=None):
    """Retorna la ruta para resolver el problema, o `None` si no se encontró
    una solución.

    :param `estado0`: estado inicial
    :param `gen_estados_alcanzables` función que recibe un estado y genera los
        estados alcanzables a partir de este
    :param `es_estado_objetivo`: función que recibe un estado e indica si es el
        estado objetivo
    :param `max_profundidad`: profundidad máxima de búsqueda; no se sigue
        buscando soluciones de más de `max_profundidad` pasos
    """
    frontera = deque([estado0]) 
    print(frontera) # estados por visitar
    ruta = []
    lista = []
    contador = 0
    pendientes = [1]  # `pendientes[i]` es el número de hijos de `ruta[i-1]`
                      # pendientes por visitar

    # FIXME: no encuentra la solución si el estado inicial es el estado
    # objetivo
    print('Buscando solución...')
    for pasos in contador_pasos or ContadorPasos():
        print("x ", pasos)
        estado = frontera.pop()
        print("ESTADO: ", estado)
        ruta.append(estado)
        pendientes[-1] -= 1

        if ((profundidad := len(ruta) - 1) < max_profundidad and (hijos := [
                hijo for hijo in gen_estados_alcanzables(estado)
                if hijo not in ruta and hijo not in frontera] )):
            if any(es_estado_objetivo(objetivo := hijo, estadoF) for hijo in hijos):
                ruta.append(objetivo)
                return ruta, pasos
            frontera.extend(hijos)
            pendientes.append(len(hijos))
        else:
            # Se retiran los estados cuyos hijos ya fueron visitados:
            pendientes.append(0)
            while (pendientes[-1] == 0):
                ruta.pop()
                pendientes.pop()
                if not ruta:
                    return None  # no resuelto


def buscar_en_profundidad(
        estado0, gen_estados_alcanzables, es_estado_objetivo, estadoF):
    contador_pasos = ContadorPasos()
    print('Buscando solución...')
    print(sys.getrecursionlimit())
    profundidad = 0
    for max_profundidad in range(1, sys.getrecursionlimit()):
        contador_pasos.send(f'{max_profundidad=}:')
        if (profundidad := _buscar_limite_profundidad(
                estado0, gen_estados_alcanzables, es_estado_objetivo,
                max_profundidad, estadoF,contador_pasos)):
            break
    print(f'profundidad: {profundidad}')
    ruta, num = _buscar_profundidad(
        estado0, gen_estados_alcanzables, es_estado_objetivo, profundidad, estadoF, contador_pasos)
    return ruta, num


