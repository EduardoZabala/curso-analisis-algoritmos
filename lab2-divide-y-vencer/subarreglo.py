"""Subarreglo maximo: fuerza bruta y divide y venceras.

Ambas soluciones buscan la mejor racha de una tienda de la cooperativa:
el tramo de dias consecutivos cuya variacion de caja acumulada es la
mayor del historial. Ninguna funcion modifica la lista recibida.
"""


def subarreglo_fuerza_bruta(valores: list[float]) -> tuple[int, int, float]:
    """Encuentra la mejor racha probando todos los pares de dias (i, j).

    Para cada dia inicial i recorre los dias finales j >= i acumulando la
    suma del tramo valores[i..j], de modo que cada par cuesta O(1) en vez
    de volver a sumar el tramo desde cero.

    Args:
        valores: variacion diaria de caja, una por dia. Tiene al menos
            un elemento.

    Returns:
        Una tupla (inicio, fin, suma) con los indices inclusivos del
        tramo de mayor suma y el valor de esa suma.
    """
    n = len(valores)
    mejor_inicio, mejor_fin = 0, 0
    mejor_suma = valores[0]

    for i in range(n):
        suma = 0
        for j in range(i, n):
            suma += valores[j]
            if suma > mejor_suma:
                mejor_inicio, mejor_fin, mejor_suma = i, j, suma

    return mejor_inicio, mejor_fin, mejor_suma


def suma_cruzada(
    valores: list[float], inicio: int, medio: int, fin: int
) -> tuple[int, int, float]:
    """Encuentra el mejor tramo que cruza el punto medio.

    Hace dos barridos lineales: uno desde medio hacia inicio y otro desde
    medio + 1 hacia fin, guardando en cada direccion la mayor suma
    acumulada y el indice donde se alcanzo. El tramo cruzado es la union
    de los dos mejores lados, asi que incluye al menos un elemento de cada
    mitad.

    Args:
        valores: variacion diaria de caja.
        inicio: indice inicial del rango considerado (inclusive).
        medio: indice del ultimo elemento de la mitad izquierda.
        fin: indice final del rango considerado (inclusive).

    Returns:
        Una tupla (inicio, fin, suma) del mejor tramo que incluye al
        menos un elemento de cada mitad.
    """
    suma = 0
    mejor_izquierda = float("-inf")
    indice_izquierda = medio
    for i in range(medio, inicio - 1, -1):
        suma += valores[i]
        if suma > mejor_izquierda:
            mejor_izquierda = suma
            indice_izquierda = i

    suma = 0
    mejor_derecha = float("-inf")
    indice_derecha = medio + 1
    for j in range(medio + 1, fin + 1):
        suma += valores[j]
        if suma > mejor_derecha:
            mejor_derecha = suma
            indice_derecha = j

    return indice_izquierda, indice_derecha, mejor_izquierda + mejor_derecha


def subarreglo_maximo(
    valores: list[float], inicio: int, fin: int
) -> tuple[int, int, float]:
    """Encuentra la mejor racha por divide y venceras.

    Divide el rango en inicio..medio y medio + 1..fin, resuelve cada mitad
    recursivamente (caso izquierdo y caso derecho), calcula el mejor tramo
    que cruza el punto medio (caso cruzado) y devuelve el mejor de los tres.
    Trabaja con indices sobre la misma lista, sin copiar porciones.

    Args:
        valores: variacion diaria de caja.
        inicio: indice inicial del rango a considerar (inclusive).
        fin: indice final del rango a considerar (inclusive).

    Returns:
        Una tupla (inicio, fin, suma) del mejor tramo dentro de
        valores[inicio..fin].
    """
    if inicio == fin:
        return inicio, fin, valores[inicio]

    medio = (inicio + fin) // 2
    izquierdo = subarreglo_maximo(valores, inicio, medio)
    derecho = subarreglo_maximo(valores, medio + 1, fin)
    cruzado = suma_cruzada(valores, inicio, medio, fin)

    if izquierdo[2] >= derecho[2] and izquierdo[2] >= cruzado[2]:
        return izquierdo
    if derecho[2] >= cruzado[2]:
        return derecho
    return cruzado
