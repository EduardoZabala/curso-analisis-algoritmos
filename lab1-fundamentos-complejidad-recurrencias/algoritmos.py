"""Algoritmos de ordenamiento instrumentados para el Laboratorio 1.

Los dos algoritmos ordenan los indices de riesgo de MAYOR A MENOR, que es
el orden que necesita la lista de llamadas de la plataforma Tamiza: el
paciente con mayor indice de riesgo debe quedar en la primera posicion.

Ambas funciones retornan una lista nueva (no modifican la lista recibida)
y el numero de comparaciones entre elementos de la lista que realizaron.
No se cuentan comparaciones de indices (j >= 0) ni de limites de ciclo.
"""


def insertion_sort(datos: list[int]) -> tuple[list[int], int]:
    """Ordena una lista de indices de riesgo con el metodo de insercion.

    No modifica la lista recibida: trabaja sobre una copia.

    Args:
        datos: lista de indices de riesgo a ordenar.

    Returns:
        Una tupla con la lista ordenada y el numero total de
        comparaciones entre elementos realizadas durante el proceso.
    """
    arreglo = list(datos)          # copia: la lista recibida no se altera
    comparaciones = 0

    for i in range(1, len(arreglo)):
        clave = arreglo[i]         # elemento que se va a insertar
        j = i - 1                  # ultimo indice de la parte ya ordenada

        # Desplaza a la derecha todo elemento MENOR que 'clave', porque el
        # orden buscado es de mayor a menor.
        while j >= 0:
            comparaciones += 1     # comparacion entre arreglo[j] y clave
            if arreglo[j] >= clave:
                break
            arreglo[j + 1] = arreglo[j]
            j -= 1

        arreglo[j + 1] = clave     # inserta 'clave' en su lugar correcto

    return arreglo, comparaciones


def merge_sort(datos: list[int]) -> tuple[list[int], int]:
    """Ordena una lista de indices de riesgo con el metodo de mezcla.

    No modifica la lista recibida: trabaja sobre una copia.

    Args:
        datos: lista de indices de riesgo a ordenar.

    Returns:
        Una tupla con la lista ordenada y el numero total de
        comparaciones entre elementos realizadas durante el proceso.
    """
    arreglo = list(datos)          # copia: la lista recibida no se altera

    if len(arreglo) <= 1:
        return arreglo, 0

    mitad = len(arreglo) // 2
    izquierda, comp_izq = merge_sort(arreglo[:mitad])
    derecha, comp_der = merge_sort(arreglo[mitad:])

    combinada, comp_merge = merge(izquierda, derecha)
    return combinada, comp_izq + comp_der + comp_merge


def merge(izquierda: list[int], derecha: list[int]) -> tuple[list[int], int]:
    """Combina dos listas ordenadas de mayor a menor en una sola.

    Recorre ambas listas en paralelo comparando los elementos al frente
    y copiando primero el mayor, hasta agotar una de las dos; despues
    copia lo que quede de la otra.

    Args:
        izquierda: lista ordenada de mayor a menor.
        derecha: lista ordenada de mayor a menor.

    Returns:
        Una tupla con la lista combinada (ordenada de mayor a menor) y el
        numero de comparaciones entre elementos realizadas en la mezcla.
    """
    resultado: list[int] = []
    comparaciones = 0
    i = j = 0

    while i < len(izquierda) and j < len(derecha):
        comparaciones += 1         # comparacion entre dos elementos
        if izquierda[i] >= derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1

    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])
    return resultado, comparaciones
