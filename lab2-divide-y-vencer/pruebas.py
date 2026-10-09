"""Pruebas de las dos soluciones del subarreglo maximo.

Se comparan sumas y no indices, porque si hay varios tramos con la misma
suma maxima cualquiera es valido. Aun asi se comprueba que los indices
devueltos sean coherentes: que el tramo exista y que sume lo reportado.

Uso:
    python pruebas.py
"""

import random

from subarreglo import subarreglo_fuerza_bruta, subarreglo_maximo, suma_cruzada

SEMILLA = 2026


def dyv(valores: list[float]) -> tuple[int, int, float]:
    """Atajo: subarreglo_maximo sobre la lista completa."""
    return subarreglo_maximo(valores, 0, len(valores) - 1)


def comprobar(valores: list[float], suma_esperada: float, nombre: str) -> None:
    """Verifica suma, indices y no modificacion con ambos algoritmos."""
    copia = list(valores)
    resultados = (("fuerza bruta", subarreglo_fuerza_bruta(valores)),
                  ("divide y venceras", dyv(valores)))
    for algoritmo, resultado in resultados:
        inicio, fin, suma = resultado
        assert suma == suma_esperada, (
            f"{nombre}: {algoritmo} dio {suma}, se esperaba {suma_esperada}")
        assert 0 <= inicio <= fin < len(valores), (
            f"{nombre}: {algoritmo} devolvio indices {inicio}, {fin}")
        assert sum(valores[inicio:fin + 1]) == suma, (
            f"{nombre}: el tramo [{inicio}, {fin}] no suma {suma}")
    assert valores == copia, f"{nombre}: alguna funcion modifico la lista"
    print(f"  OK  {nombre}: suma {suma_esperada}")


# 1. Serie de ocho dias de la situacion problema: dias 2 a 7, suma 17.
serie = [-3, 5, -2, 8, -6, 3, 9, -4]
assert subarreglo_fuerza_bruta(serie)[2] == 17
assert subarreglo_maximo(serie, 0, len(serie) - 1)[2] == 17
assert dyv(serie)[:2] == (1, 6), "la racha debe ir del dia 2 al dia 7"
comprobar(serie, 17, "serie de ocho dias")

# 2. Un solo elemento: el unico tramo posible es ese dia (positivo o negativo).
comprobar([7], 7, "un elemento positivo")
comprobar([-4], -4, "un elemento negativo")

# 3. Todos negativos: la mejor racha es el dia menos malo, no una suma vacia.
comprobar([-8, -3, -6, -2, -5, -9], -2, "todos negativos")

# 4. Todos positivos: la mejor racha es la serie completa.
positivos = [4, 1, 7, 3, 2, 6, 5]
comprobar(positivos, sum(positivos), "todos positivos")

# 5. Caso cruzado: las dos mitades por separado valen poco, pero el mejor
#    tramo toma el final de la izquierda y el inicio de la derecha.
#    Mitad izquierda [-10, -1, 6, 5] -> mejor 11; derecha [4, 3, -1, -10]
#    -> mejor 7; el tramo cruzado [6, 5, 4, 3] suma 18.
cruzado = [-10, -1, 6, 5, 4, 3, -1, -10]
comprobar(cruzado, 18, "mejor tramo cruza el punto medio")
assert dyv(cruzado)[:2] == (2, 5)
assert suma_cruzada(cruzado, 0, 3, 7) == (2, 5, 18)
# suma_cruzada siempre toma al menos un elemento de cada lado, aunque ese
# lado solo reste: aqui la derecha aporta su "mejor" perdida, -1.
assert suma_cruzada([5, -1, -2], 0, 1, 2) == (0, 2, 2)

# 6. Empates y ceros: varias rachas con la misma suma; solo importa la suma.
comprobar([3, -3, 3, -3, 3], 3, "empates entre tramos")
comprobar([0, 0, 0], 0, "todos ceros")

# 7. Al menos veinte listas aleatorias: ambas funciones dan la misma suma.
generador = random.Random(SEMILLA)
casos_aleatorios = 200
for k in range(casos_aleatorios):
    n = generador.randint(1, 120)
    valores = [generador.randint(-100, 100) for _ in range(n)]
    copia = list(valores)
    suma_fb = subarreglo_fuerza_bruta(valores)[2]
    suma_dyv = dyv(valores)[2]
    assert suma_fb == suma_dyv, (
        f"lista {k} (n={n}): fuerza bruta {suma_fb} vs dyv {suma_dyv}")
    assert valores == copia
print(f"  OK  {casos_aleatorios} listas aleatorias (n de 1 a 120, "
      f"semilla {SEMILLA}): ambas funciones coinciden")

# 8. Valores decimales: las funciones aceptan float, no solo enteros.
decimales = [1.5, -0.5, 2.25, -4.0, 3.0]
assert dyv(decimales)[2] == subarreglo_fuerza_bruta(decimales)[2] == 3.25
print("  OK  valores decimales: suma 3.25")

print("\nTodas las pruebas pasaron.")
