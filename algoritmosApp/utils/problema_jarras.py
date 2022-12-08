"""Estructuras de datos y funciones útiles para resolver el problema de las
jarras.
"""

from collections import namedtuple


JarraConteniendo = namedtuple('Jarra', ['contenido', 'capacidad'])
# Retorna una copia de la jarra pero con un nuevo contenido:
JarraConteniendo.conteniendo = (
    lambda self, contenido: JarraConteniendo(contenido, self.capacidad))
Jarra = lambda capacidad: JarraConteniendo(0, capacidad)


def accion(accion_):
    """Las acciones serán funciones puras, por lo tanto no deben mutar el
    estado. Esta función recibe una acción y la invoca con una copia mutable
    del estado para mayor conveniencia, luego convierte el estado resultante en
    una estructura inmutable nuevamente.
    """
    def accion_pura(jarras, *args, **kwargs):
        jarras = list(jarras)  # copia mutable
        accion_(jarras, *args, **kwargs)
        return tuple(jarras)  # copia hasheable y por tanto inmutable
    return accion_pura


@accion
def llenar_jarra(jarras, i):
    jarras[i] = jarras[i].conteniendo(jarras[i].capacidad)


@accion
def vaciar_jarra(jarras, i):
    jarras[i] = jarras[i].conteniendo(0)


@accion
def vaciar_jarra_en(jarras, i, j):
    j1, j2 = jarras[i], jarras[j]
    cantidad = min(j1.contenido, j2.capacidad - j2.contenido)
    jarras[i] = j1.conteniendo(j1.contenido - cantidad)
    jarras[j] = j2.conteniendo(j2.contenido + cantidad)


def gen_sucesores(jarras):
    """
    indices = range(len(jarras))
    yield from (llenar_jarra(jarras, i) for i in indices)
    yield from (vaciar_jarra(jarras, i) for i in indices)
    yield from (vaciar_jarra_en(jarras, i, j)
                for i in indices for j in indices if i != j)
    """
    for i in range(len(jarras)):
        yield llenar_jarra(jarras, i)
        yield vaciar_jarra(jarras, i)
        yield from (vaciar_jarra_en(jarras, i, j)
                    for j in range(len(jarras)) if i != j)


def crear_test_objetivo(objetivo):
    """Retorna una función que recibe un estado y determina si es un estado
    objetivo.
    """
    def test_objetivo(jarras):
        return any(jarra.contenido == objetivo for jarra in jarras)
    return test_objetivo
