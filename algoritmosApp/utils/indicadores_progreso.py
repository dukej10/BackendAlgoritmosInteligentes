"""Objetos para visualizar el progreso de un algoritmo."""

from itertools import count


def _corrutina(f):
    def corrutina_preparada(*args, **kwargs):
        corrutina = f(*args, **kwargs)
        next(corrutina)  # preparar la corrutina (to prime it)
        return corrutina
    return corrutina_preparada


@_corrutina
def ContadorPasosSimple():
    """Imprime el número de pasos en líneas separadas."""
    for paso in count(start=1):
        while rec := (yield paso):
            continue
        #print(paso)


def ContadorPasos():
    """Crea un iterador que imprime y retorna el número de pasos que lleva un
    algoritmo en cada iteración.
    """
    return ContadorPasosSimple()
