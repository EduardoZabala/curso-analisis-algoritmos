"""Generadores de lotes de registros para los escenarios de Tamiza.

Cada generador produce una lista de n indices de riesgo enteros
distintos entre si. Para garantizar que no haya valores repetidos con
n grande, los indices se toman como multiplos de 10 en el rango
[10, n * 10]; el orden en que quedan es lo que distingue un escenario
de otro. El orden que el algoritmo debe producir es de MAYOR A MENOR.
"""

import random


def _base_descendente(n: int) -> list[int]:
    """Construye n indices distintos ya ordenados de mayor a menor.

    Args:
        n: cantidad de registros del lote.

    Returns:
        Lista de n enteros distintos en orden descendente, construida
        directamente (sin usar ninguna rutina de ordenamiento).
    """
    return list(range(n * 10, 0, -10))


def generar_aleatorio(n: int, semilla: int = 42) -> list[int]:
    """Genera un lote de n registros en orden aleatorio (escenario A).

    Args:
        n: cantidad de registros del lote.
        semilla: semilla del generador aleatorio, para que el
            experimento sea reproducible.

    Returns:
        Lista de n indices de riesgo enteros distintos, desordenada.
    """
    lote = _base_descendente(n)
    random.Random(semilla).shuffle(lote)
    return lote


def generar_casi_ordenado(n: int, semilla: int = 42) -> list[int]:
    """Genera un lote casi ordenado: 98% ordenado y 2% al final (escenario B).

    Args:
        n: cantidad de registros del lote.
        semilla: semilla del generador aleatorio.

    Returns:
        Lista de n indices de riesgo enteros distintos, con el primer
        98% en el orden que el algoritmo produce y el 2% restante
        desordenado al final.
    """
    aleatorio = random.Random(semilla)
    base = _base_descendente(n)

    # El 2% son los resultados nuevos del dia: se retiran de la lista de
    # ayer y se anexan al final sin ordenar. Sus indices de riesgo pueden
    # ser cualesquiera, por eso se eligen en posiciones al azar.
    nuevos_cantidad = max(1, round(n * 0.02)) if n > 1 else 0
    posiciones_nuevos = set(aleatorio.sample(range(n), nuevos_cantidad))

    lista_de_ayer = [v for i, v in enumerate(base)
                     if i not in posiciones_nuevos]
    nuevos = [v for i, v in enumerate(base) if i in posiciones_nuevos]
    aleatorio.shuffle(nuevos)

    return lista_de_ayer + nuevos


def generar_inverso(n: int) -> list[int]:
    """Genera un lote en el orden exactamente contrario (escenario C).

    Args:
        n: cantidad de registros del lote.

    Returns:
        Lista de n indices de riesgo enteros distintos, en el orden
        inverso al que el algoritmo debe producir.
    """
    return list(range(10, n * 10 + 1, 10))


def generar_ordenado(n: int) -> list[int]:
    """Genera un lote ya ordenado como el algoritmo lo necesita.

    No corresponde a ningun canal de Tamiza: se usa solo como control
    del mejor caso teorico de insertion sort, para contrastarlo con el
    escenario B.

    Args:
        n: cantidad de registros del lote.

    Returns:
        Lista de n indices de riesgo enteros distintos, en orden
        descendente.
    """
    return _base_descendente(n)
