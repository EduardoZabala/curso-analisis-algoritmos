"""Parte 4 - Validacion experimental de la complejidad de los dos algoritmos.

Mide insertion_sort y merge_sort sobre el escenario A de Tamiza (cargue
aleatorio desde el portal) con los mismos tamanos de la Parte 3, genera
la grafica graficas/parte4_tiempo.png y extrapola el tiempo que tomaria
cada algoritmo con los 1.200.000 registros del proceso nocturno.

Uso:
    python parte4_complejidad.py
"""

import math
import time
from collections import Counter
from collections.abc import Callable
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # backend sin ventana: debe fijarse antes de importar
# pyplot, por eso los imports siguientes no van al inicio del archivo.
import matplotlib.pyplot as plt  # noqa: E402

from algoritmos import insertion_sort, merge_sort  # noqa: E402
from datos import (generar_aleatorio, generar_casi_ordenado,  # noqa: E402
                   generar_inverso)

# Firma de un algoritmo de ordenamiento instrumentado: recibe la lista de
# indices de riesgo y retorna la lista ordenada y el conteo de comparaciones.
Ordenador = Callable[[list[int]], tuple[list[int], int]]

TAMANOS = [100, 200, 400, 800, 1600, 3200, 6400, 12800]
SEMILLA = 42
REGISTROS_TAMIZA = 1_200_000
VENTANA_SEGUNDOS = 4 * 3600
POTENCIA_SERVIDOR_W = 450  # supuesto de carga sostenida, igual al de clase
CARPETA_GRAFICAS = Path(__file__).parent / "graficas"


def medir(algoritmo: Ordenador, lote: list[int]) -> tuple[float, int]:
    """Cronometra una ejecucion del algoritmo sobre un lote ya generado.

    Args:
        algoritmo: funcion que recibe una lista y retorna la lista
            ordenada junto con el numero de comparaciones.
        lote: datos de entrada, generados de antemano.

    Returns:
        Una tupla con el tiempo en segundos y el numero de comparaciones.
    """
    inicio = time.perf_counter()
    _, comparaciones = algoritmo(lote)
    fin = time.perf_counter()
    return fin - inicio, comparaciones


def ejecutar_experimento() -> dict[str, dict[str, list]]:
    """Mide los dos algoritmos sobre el escenario A para todos los tamanos.

    Returns:
        Diccionario algoritmo -> {"tiempos": [...], "comparaciones": [...]}.
    """
    algoritmos = {"Insertion sort": insertion_sort, "Merge sort": merge_sort}
    resultados: dict[str, dict[str, list]] = {
        nombre: {"tiempos": [], "comparaciones": []} for nombre in algoritmos
    }

    for nombre, algoritmo in algoritmos.items():
        for n in TAMANOS:
            lote = generar_aleatorio(n, SEMILLA)  # fuera del cronometro
            repeticiones = 3 if n <= 3200 else 1
            mejor_tiempo = float("inf")
            comparaciones = 0
            for _ in range(repeticiones):
                tiempo, comparaciones = medir(algoritmo, lote)
                mejor_tiempo = min(mejor_tiempo, tiempo)
            resultados[nombre]["tiempos"].append(mejor_tiempo)
            resultados[nombre]["comparaciones"].append(comparaciones)

    return resultados


def medir_merge_en_los_tres_escenarios() -> dict[str, float]:
    """Mide merge_sort en A, B y C con el tamano mas grande del experimento.

    Sirve para sustentar en el concepto tecnico que merge sort no cambia
    de comportamiento segun el canal de entrada.

    Returns:
        Diccionario escenario -> tiempo en segundos.
    """
    n = TAMANOS[-1]
    lotes = {
        "A - Aleatorio": generar_aleatorio(n, SEMILLA),
        "B - Casi ordenado": generar_casi_ordenado(n, SEMILLA),
        "C - Orden inverso": generar_inverso(n),
    }
    return {nombre: medir(merge_sort, lote)[0]
            for nombre, lote in lotes.items()}


def verificar_equivalencia() -> None:
    """Comprueba los dos algoritmos sobre los tres escenarios de Tamiza.

    Para cada escenario verifica que ninguno de los dos algoritmos altera
    la lista recibida, que ambos conservan los mismos elementos de la
    entrada, que ambos ordenan de mayor a menor y que sus salidas
    coinciden entre si.

    Raises:
        AssertionError: si alguno de los tres escenarios falla.
    """
    escenarios = {
        "A - Aleatorio": generar_aleatorio(400, SEMILLA),
        "B - Casi ordenado": generar_casi_ordenado(400, SEMILLA),
        "C - Orden inverso": generar_inverso(400),
    }

    for nombre, lote in escenarios.items():
        copia = list(lote)
        por_insercion, _ = insertion_sort(lote)
        por_mezcla, _ = merge_sort(lote)

        assert lote == copia, (
            f"algun algoritmo modifico la lista recibida en {nombre}")
        for algoritmo, salida in (("insertion_sort", por_insercion),
                                  ("merge_sort", por_mezcla)):
            assert Counter(salida) == Counter(copia), (
                f"{algoritmo} no conserva los elementos en {nombre}")
            assert all(
                salida[i] >= salida[i + 1] for i in range(len(salida) - 1)
            ), f"{algoritmo} no ordeno de mayor a menor en {nombre}"
        assert por_insercion == por_mezcla, (
            f"las salidas de los dos algoritmos difieren en {nombre}")
        print(f"  {nombre}: ambos algoritmos ordenan igual y correctamente")

    print("Verificacion de los dos algoritmos en los tres escenarios: OK\n")


def graficar(resultados: dict[str, dict[str, list]]) -> None:
    """Dibuja tiempo vs. tamano de entrada, una curva por algoritmo.

    El panel izquierdo usa escala lineal, donde se ve la forma cuadratica
    de insertion sort; el derecho usa escala logaritmica en ambos ejes,
    donde la curva de merge sort deja de quedar aplastada contra el eje.

    Args:
        resultados: salida de ejecutar_experimento().
    """
    CARPETA_GRAFICAS.mkdir(exist_ok=True)
    figura, ejes = plt.subplots(1, 2, figsize=(13, 5.5))

    marcadores = {"Insertion sort": "o", "Merge sort": "s"}
    for eje, escala in zip(ejes, ("lineal", "log-log")):
        for nombre, datos in resultados.items():
            eje.plot(TAMANOS, datos["tiempos"], marker=marcadores[nombre],
                     label=nombre)
        if escala == "log-log":
            eje.set_xscale("log")
            eje.set_yscale("log")
        eje.set_title(f"Escala {escala}")
        eje.set_xlabel("Tamano de la entrada n (numero de registros)")
        eje.set_ylabel("Tiempo de ejecucion (segundos)")
        eje.legend()
        eje.grid(True, which="both", linestyle=":", alpha=0.6)

    figura.suptitle("Insertion sort vs. merge sort: tiempo de ejecucion "
                    "(escenario A de Tamiza, cargue aleatorio)")
    figura.tight_layout()
    figura.savefig(CARPETA_GRAFICAS / "parte4_tiempo.png", dpi=150)
    plt.close(figura)
    print("Grafica escrita: graficas/parte4_tiempo.png")


def extrapolar(resultados: dict[str, dict[str, list]]) -> None:
    """Estima el tiempo con 1.200.000 registros a partir de la medicion mayor.

    Ajusta la constante oculta de cada modelo asintotico con el punto
    medido mas grande (insertion sort con n^2, merge sort con n log2 n) y
    evalua ese modelo en n = 1.200.000. Es una estimacion, no una medida.
    """
    n_ref = TAMANOS[-1]
    t_insercion = resultados["Insertion sort"]["tiempos"][-1]
    t_mezcla = resultados["Merge sort"]["tiempos"][-1]

    c_insercion = t_insercion / (n_ref ** 2)
    c_mezcla = t_mezcla / (n_ref * math.log2(n_ref))

    est_insercion = c_insercion * REGISTROS_TAMIZA ** 2
    est_mezcla = c_mezcla * REGISTROS_TAMIZA * math.log2(REGISTROS_TAMIZA)

    print(f"Punto de referencia medido: n = {n_ref:,}")
    print(f"  insertion sort: {t_insercion:.4f} s  ->  c = {c_insercion:.3e}")
    print(f"  merge sort:     {t_mezcla:.4f} s  ->  c = {c_mezcla:.3e}\n")

    print(f"Extrapolacion a n = {REGISTROS_TAMIZA:,} registros (estimacion):")
    for nombre, segundos in (("insertion sort", est_insercion),
                             ("merge sort", est_mezcla)):
        horas = segundos / 3600
        cabe = "SI cabe" if segundos <= VENTANA_SEGUNDOS else "NO cabe"
        kwh_anio = (POTENCIA_SERVIDOR_W / 1000) * horas * 365
        print(f"  {nombre}: {segundos:,.0f} s = {horas:,.2f} h "
              f"({cabe} en la ventana de 4 h); "
              f"~{kwh_anio:,.0f} kWh/anio a {POTENCIA_SERVIDOR_W} W")
    razon = est_insercion / est_mezcla
    print(f"  razon insertion/merge: {razon:,.0f} veces\n")

    # Mismo ejercicio para el peor caso de insertion sort (escenario C), que
    # es el que decide si el sistema entra o no en produccion.
    t_peor = medir(insertion_sort, generar_inverso(n_ref))[0]
    est_peor = (t_peor / n_ref ** 2) * REGISTROS_TAMIZA ** 2
    horas_peor = est_peor / 3600
    print(f"Peor caso (escenario C) medido en n = {n_ref:,}: {t_peor:.4f} s")
    print(f"  extrapolado a {REGISTROS_TAMIZA:,}: {est_peor:,.0f} s "
          f"= {horas_peor:,.2f} h")
    print(f"  con un servidor del doble de velocidad: {horas_peor / 2:,.2f} h")
    print(f"  escenario A con el doble de velocidad: "
          f"{est_insercion / 3600 / 2:,.2f} h\n")


def imprimir_tabla(resultados: dict[str, dict[str, list]]) -> None:
    """Imprime los resultados como tabla Markdown lista para el informe."""
    print("| n | Tiempo insertion sort (s) | Tiempo merge sort (s) "
          "| Comparaciones insertion sort | Comparaciones merge sort |")
    print("| --- | --- | --- | --- | --- |")
    for indice, n in enumerate(TAMANOS):
        t_i = resultados["Insertion sort"]["tiempos"][indice]
        t_m = resultados["Merge sort"]["tiempos"][indice]
        c_i = resultados["Insertion sort"]["comparaciones"][indice]
        c_m = resultados["Merge sort"]["comparaciones"][indice]
        print(f"| {n} | {t_i:.6f} | {t_m:.6f} | {c_i:,} | {c_m:,} |")
    print()


def main() -> None:
    """Corre la verificacion, el experimento, la grafica y la extrapolacion."""
    verificar_equivalencia()
    resultados = ejecutar_experimento()
    imprimir_tabla(resultados)
    graficar(resultados)
    extrapolar(resultados)

    print(f"Merge sort en los tres escenarios con n = {TAMANOS[-1]:,}:")
    for nombre, tiempo in medir_merge_en_los_tres_escenarios().items():
        print(f"  {nombre}: {tiempo:.4f} s")


if __name__ == "__main__":
    main()
