"""Parte 2 - Medicion del tiempo de ejecucion de las dos soluciones.

Mide subarreglo_fuerza_bruta y subarreglo_maximo sobre series de variacion
de caja generadas con semilla fija, verifica en cada tamano que ambos
devuelven la misma suma, genera la grafica graficas/tiempo_vs_n.png e
imprime la tabla, los factores de crecimiento al duplicar n y la
estimacion para una serie de 1.000.000 de registros.

Uso:
    python medicion.py
"""

import gc
import math
import random
import statistics
import time
from collections.abc import Callable
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # backend sin ventana: debe fijarse antes de importar
# pyplot, por eso los imports siguientes no van al inicio del archivo.
import matplotlib.pyplot as plt  # noqa: E402

from subarreglo import subarreglo_fuerza_bruta, subarreglo_maximo  # noqa: E402

# Firma comun de las dos soluciones una vez se fija el rango completo.
Solucion = Callable[[list[float]], tuple[int, int, float]]

# Siete tamanos menores de 100 para ubicar el cruce entre las curvas y,
# desde 125, una cadena donde n se duplica en cada paso hasta 8000.
TAMANOS = [5, 10, 15, 20, 30, 50, 75, 125, 250, 500, 1000, 2000, 4000, 8000]
SEMILLA = 42
VALOR_MINIMO, VALOR_MAXIMO = -100, 100
REGISTROS_OBJETIVO = 1_000_000
TIENDAS, DIAS_POR_TIENDA = 1_500, 2_000
CARPETA_GRAFICAS = Path(__file__).parent / "graficas"
COLORES = {"Fuerza bruta": "#eb6834", "Divide y venceras": "#2a78d6"}
MARCADORES = {"Fuerza bruta": "o", "Divide y venceras": "s"}


def divide_y_venceras(valores: list[float]) -> tuple[int, int, float]:
    """Llama a subarreglo_maximo sobre la serie completa.

    Args:
        valores: variacion diaria de caja, con al menos un elemento.

    Returns:
        La tupla (inicio, fin, suma) del mejor tramo de toda la serie.
    """
    return subarreglo_maximo(valores, 0, len(valores) - 1)


SOLUCIONES: dict[str, Solucion] = {
    "Fuerza bruta": subarreglo_fuerza_bruta,
    "Divide y venceras": divide_y_venceras,
}


def generar_serie(n: int) -> list[int]:
    """Genera una serie reproducible de n variaciones de caja.

    Args:
        n: numero de dias de la serie.

    Returns:
        Lista de n enteros entre VALOR_MINIMO y VALOR_MAXIMO. Con la misma
        semilla y el mismo n la lista es siempre la misma.
    """
    generador = random.Random(SEMILLA)
    return [generador.randint(VALOR_MINIMO, VALOR_MAXIMO) for _ in range(n)]


def repeticiones_para(n: int) -> int:
    """Decide cuantas veces se repite la medicion de un tamano.

    Los tamanos pequenos tardan microsegundos y el ruido del sistema pesa
    mas, por eso se repiten mas veces. Los grandes tambien se repiten (cinco
    veces) para no depender de una sola corrida.

    Args:
        n: tamano de la entrada.

    Returns:
        Numero de repeticiones de la medicion.
    """
    if n <= 100:
        return 101
    if n <= 1000:
        return 21
    return 5


def cronometrar(solucion: Solucion, valores: list[float]) -> float:
    """Mide una sola llamada al algoritmo con time.perf_counter().

    El recolector de basura se apaga solo durante la llamada para que una
    pausa suya no se cuente como tiempo del algoritmo.

    Args:
        solucion: algoritmo a medir.
        valores: serie ya generada; su generacion queda fuera del reloj.

    Returns:
        Tiempo de la llamada en segundos.
    """
    gc.disable()
    try:
        inicio = time.perf_counter()
        solucion(valores)
        fin = time.perf_counter()
    finally:
        gc.enable()
    return fin - inicio


def ejecutar_experimento() -> dict[str, list[float]]:
    """Mide ambos algoritmos en todos los tamanos y verifica sus sumas.

    Para cada tamano se genera una sola lista, que reciben los dos
    algoritmos. Antes de medir se comprueba que ambos devuelven la misma
    suma; luego cada medicion se repite y se guarda la mediana.

    Returns:
        Diccionario algoritmo -> lista de medianas en segundos, alineada
        con TAMANOS.

    Raises:
        AssertionError: si en algun tamano las sumas no coinciden.
    """
    resultados: dict[str, list[float]] = {nombre: [] for nombre in SOLUCIONES}

    for n in TAMANOS:
        valores = generar_serie(n)
        copia = list(valores)
        suma_fb = subarreglo_fuerza_bruta(valores)[2]
        suma_dyv = divide_y_venceras(valores)[2]
        assert suma_fb == suma_dyv, (
            f"n={n}: fuerza bruta {suma_fb} vs divide y venceras {suma_dyv}")
        assert valores == copia, f"n={n}: se modifico la lista de entrada"

        repeticiones = repeticiones_para(n)
        for nombre, solucion in SOLUCIONES.items():
            tiempos = [cronometrar(solucion, valores)
                       for _ in range(repeticiones)]
            resultados[nombre].append(statistics.median(tiempos))
        print(f"  n={n:>5}: suma maxima {suma_fb:>6} en ambos "
              f"({repeticiones} repeticiones)")

    print("Verificacion: ambos algoritmos coinciden en todos los tamanos\n")
    return resultados


def graficar(resultados: dict[str, list[float]]) -> None:
    """Dibuja tiempo vs. tamano de entrada con ambas curvas en los mismos ejes.

    El panel izquierdo usa escala lineal, donde se ve la forma de cada
    curva; el derecho usa escala logaritmica en ambos ejes, donde los
    tamanos pequenos y el cruce entre las curvas se pueden leer.

    Args:
        resultados: salida de ejecutar_experimento().
    """
    CARPETA_GRAFICAS.mkdir(exist_ok=True)
    figura, ejes = plt.subplots(1, 2, figsize=(13, 5.5))

    for eje, escala in zip(ejes, ("lineal", "log-log")):
        for nombre, tiempos in resultados.items():
            milisegundos = [t * 1000 for t in tiempos]
            eje.plot(TAMANOS, milisegundos, marker=MARCADORES[nombre],
                     markersize=6, linewidth=2, color=COLORES[nombre],
                     label=nombre)
        if escala == "log-log":
            eje.set_xscale("log")
            eje.set_yscale("log")
        eje.set_title(f"Escala {escala}")
        eje.set_xlabel("Tamano de la serie n (numero de dias)")
        eje.set_ylabel("Tiempo de ejecucion (milisegundos, mediana)")
        eje.legend()
        eje.grid(True, which="both", linestyle=":", alpha=0.5)

    figura.suptitle("Subarreglo maximo: fuerza bruta vs. divide y venceras "
                    "(tiempo vs. tamano de entrada)")
    figura.tight_layout()
    figura.savefig(CARPETA_GRAFICAS / "tiempo_vs_n.png", dpi=150)
    plt.close(figura)
    print("Grafica escrita: graficas/tiempo_vs_n.png\n")


def imprimir_tabla(resultados: dict[str, list[float]]) -> None:
    """Imprime los tiempos como tabla Markdown lista para el informe."""
    print("| n | Fuerza bruta (ms) | Divide y venceras (ms) "
          "| Fuerza bruta / DyV |")
    print("| ---: | ---: | ---: | ---: |")
    for indice, n in enumerate(TAMANOS):
        t_fb = resultados["Fuerza bruta"][indice]
        t_dyv = resultados["Divide y venceras"][indice]
        print(f"| {n} | {t_fb * 1000:.4f} | {t_dyv * 1000:.4f} "
              f"| {t_fb / t_dyv:.2f} |")
    print()


def imprimir_factores(resultados: dict[str, list[float]]) -> None:
    """Imprime cuanto se multiplica el tiempo cada vez que n se duplica.

    Junto al factor medido imprime el que predice cada modelo: 4 para n^2
    y 2 * log2(2n) / log2(n) para n log n.
    """
    print("| n -> 2n | Fuerza bruta | Esperado n^2 "
          "| Divide y venceras | Esperado n log n |")
    print("| --- | ---: | ---: | ---: | ---: |")
    for indice in range(len(TAMANOS) - 1):
        n, siguiente = TAMANOS[indice], TAMANOS[indice + 1]
        if siguiente != 2 * n:
            continue
        f_fb = (resultados["Fuerza bruta"][indice + 1]
                / resultados["Fuerza bruta"][indice])
        f_dyv = (resultados["Divide y venceras"][indice + 1]
                 / resultados["Divide y venceras"][indice])
        esperado_nlogn = 2 * math.log2(siguiente) / math.log2(n)
        print(f"| {n} -> {siguiente} | {f_fb:.2f} | 4.00 "
              f"| {f_dyv:.2f} | {esperado_nlogn:.2f} |")
    print()


def imprimir_cruce(resultados: dict[str, list[float]]) -> None:
    """Indica desde que tamano medido divide y venceras es mas rapido."""
    for indice, n in enumerate(TAMANOS):
        restantes = range(indice, len(TAMANOS))
        if all(resultados["Divide y venceras"][k]
               < resultados["Fuerza bruta"][k] for k in restantes):
            print(f"Divide y venceras gana en todos los tamanos desde n = {n}"
                  "\n")
            return
    print("Divide y venceras no gana de forma sostenida en el rango medido\n")


def estimar(resultados: dict[str, list[float]]) -> None:
    """Estima el tiempo con 1.000.000 de registros desde la mayor medicion.

    Ajusta la constante oculta de cada modelo con el punto medido mas
    grande (fuerza bruta con n^2, divide y venceras con n log2 n) y evalua
    el modelo en n = 1.000.000. Es una estimacion, no una medida. Tambien
    estima el lote completo de la cooperativa (1.500 tiendas de 2.000 dias).
    """
    n_ref = TAMANOS[-1]
    t_fb = resultados["Fuerza bruta"][-1]
    t_dyv = resultados["Divide y venceras"][-1]
    c_fb = t_fb / n_ref ** 2
    c_dyv = t_dyv / (n_ref * math.log2(n_ref))

    def modelo_fb(n: int) -> float:
        return c_fb * n ** 2

    def modelo_dyv(n: int) -> float:
        return c_dyv * n * math.log2(n)

    print(f"Referencia medida en n = {n_ref:,}:")
    print(f"  fuerza bruta:      {t_fb:.4f} s -> c = {c_fb:.3e} s")
    print(f"  divide y venceras: {t_dyv:.4f} s -> c = {c_dyv:.3e} s\n")

    n = REGISTROS_OBJETIVO
    est_fb, est_dyv = modelo_fb(n), modelo_dyv(n)
    print(f"Estimacion para una serie de {n:,} registros:")
    print(f"  fuerza bruta:      {est_fb:,.0f} s = {est_fb / 3600:,.2f} h")
    print(f"  divide y venceras: {est_dyv:,.2f} s")
    print(f"  razon: {est_fb / est_dyv:,.0f} veces\n")

    lote_fb = TIENDAS * modelo_fb(DIAS_POR_TIENDA)
    lote_dyv = TIENDAS * modelo_dyv(DIAS_POR_TIENDA)
    print(f"Estimacion para {TIENDAS:,} tiendas de {DIAS_POR_TIENDA:,} dias:")
    print(f"  fuerza bruta:      {lote_fb:,.0f} s = {lote_fb / 60:,.1f} min")
    print(f"  divide y venceras: {lote_dyv:,.1f} s")


def main() -> None:
    """Corre la medicion, la tabla, la grafica y la estimacion."""
    resultados = ejecutar_experimento()
    imprimir_tabla(resultados)
    imprimir_factores(resultados)
    imprimir_cruce(resultados)
    graficar(resultados)
    estimar(resultados)


if __name__ == "__main__":
    main()
