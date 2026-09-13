"""Parte 3 - Peor caso, mejor caso y caso promedio de insertion sort.

Ejecuta insertion_sort instrumentado sobre los tres escenarios de
entrada de Tamiza (A aleatorio, B casi ordenado, C orden inverso) para
ocho tamanos de entrada, y genera las dos graficas de la Parte 3:

    graficas/parte3_comparaciones.png
    graficas/parte3_tiempo.png

Uso:
    python parte3_casos.py
"""

import time
from collections import Counter
from collections.abc import Callable
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # backend sin ventana: debe fijarse antes de importar
# pyplot, por eso los imports siguientes no van al inicio del archivo.
import matplotlib.pyplot as plt  # noqa: E402

from algoritmos import insertion_sort  # noqa: E402
from datos import (generar_aleatorio, generar_casi_ordenado,  # noqa: E402
                   generar_inverso, generar_ordenado)

# Firma de un algoritmo de ordenamiento instrumentado: recibe la lista de
# indices de riesgo y retorna la lista ordenada y el conteo de comparaciones.
Ordenador = Callable[[list[int]], tuple[list[int], int]]

TAMANOS = [100, 200, 400, 800, 1600, 3200, 6400, 12800]
SEMILLA = 42
CARPETA_GRAFICAS = Path(__file__).parent / "graficas"

ESCENARIOS = {
    "A - Aleatorio": lambda n: generar_aleatorio(n, SEMILLA),
    "B - Casi ordenado": lambda n: generar_casi_ordenado(n, SEMILLA),
    "C - Orden inverso": lambda n: generar_inverso(n),
}


def repeticiones_para(n: int) -> int:
    """Define cuantas veces se repite la medicion de un tamano dado.

    Los tamanos pequenos se repiten para amortiguar el ruido del reloj;
    los grandes se miden una sola vez para no alargar el experimento.

    Args:
        n: tamano de la entrada.

    Returns:
        Numero de repeticiones de la medicion.
    """
    return 3 if n <= 3200 else 1


def medir(algoritmo: Ordenador, lote: list[int]) -> tuple[float, int]:
    """Cronometra una sola ejecucion del algoritmo sobre un lote ya generado.

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
    """Mide insertion_sort en los tres escenarios para todos los tamanos.

    Returns:
        Diccionario escenario -> {"tiempos": [...], "comparaciones": [...]}.
    """
    resultados: dict[str, dict[str, list]] = {
        nombre: {"tiempos": [], "comparaciones": []} for nombre in ESCENARIOS
    }

    for nombre, generador in ESCENARIOS.items():
        for n in TAMANOS:
            lote = generador(n)  # la generacion queda FUERA del cronometro
            mejor_tiempo = float("inf")
            comparaciones = 0
            for _ in range(repeticiones_para(n)):
                tiempo, comparaciones = medir(insertion_sort, lote)
                mejor_tiempo = min(mejor_tiempo, tiempo)
            resultados[nombre]["tiempos"].append(mejor_tiempo)
            resultados[nombre]["comparaciones"].append(comparaciones)

    return resultados


def verificar_correccion() -> None:
    """Comprueba insertion_sort sobre los tres escenarios de Tamiza.

    Para cada escenario verifica tres cosas: que la lista recibida no se
    altera, que la salida conserva exactamente los mismos elementos que
    la entrada, y que queda ordenada de mayor a menor.

    Raises:
        AssertionError: si alguno de los tres escenarios falla.
    """
    for nombre, generador in ESCENARIOS.items():
        lote = generador(400)
        copia = list(lote)
        ordenado, _ = insertion_sort(lote)

        assert lote == copia, (
            f"insertion_sort modifico la lista recibida en el escenario "
            f"{nombre}")
        assert Counter(ordenado) == Counter(copia), (
            f"la salida no conserva los mismos elementos en el escenario "
            f"{nombre}")
        assert all(
            ordenado[i] >= ordenado[i + 1] for i in range(len(ordenado) - 1)
        ), f"la salida no quedo ordenada de mayor a menor en {nombre}"
        print(f"  {nombre}: ordena correctamente y no altera la entrada")

    print("Verificacion de insertion_sort en los tres escenarios: OK\n")


def graficar(resultados: dict[str, dict[str, list]], clave: str,
             titulo: str, etiqueta_y: str, archivo: str) -> None:
    """Dibuja una metrica de los tres escenarios en los mismos ejes.

    Genera dos paneles: escala lineal, donde se ve la forma de la curva, y
    escala logaritmica en ambos ejes, donde se distinguen los escenarios
    cuyos valores quedan aplastados contra el eje en la escala lineal.

    Args:
        resultados: salida de ejecutar_experimento().
        clave: "tiempos" o "comparaciones".
        titulo: titulo de la grafica.
        etiqueta_y: rotulo del eje vertical, con unidades.
        archivo: nombre del PNG a escribir dentro de graficas/.
    """
    CARPETA_GRAFICAS.mkdir(exist_ok=True)
    figura, ejes = plt.subplots(1, 2, figsize=(13, 5.5))

    marcadores = {"A - Aleatorio": "o", "B - Casi ordenado": "s",
                  "C - Orden inverso": "^"}
    for eje, escala in zip(ejes, ("lineal", "log-log")):
        for nombre, datos in resultados.items():
            eje.plot(TAMANOS, datos[clave], marker=marcadores[nombre],
                     label=f"Escenario {nombre}")
        if escala == "log-log":
            eje.set_xscale("log")
            eje.set_yscale("log")
        eje.set_title(f"Escala {escala}")
        eje.set_xlabel("Tamano de la entrada n (numero de registros)")
        eje.set_ylabel(etiqueta_y)
        eje.legend()
        eje.grid(True, which="both", linestyle=":", alpha=0.6)

    figura.suptitle(titulo)
    figura.tight_layout()
    figura.savefig(CARPETA_GRAFICAS / archivo, dpi=150)
    plt.close(figura)
    print(f"Grafica escrita: graficas/{archivo}")


def imprimir_tabla(resultados: dict[str, dict[str, list]]) -> None:
    """Imprime los resultados como tabla Markdown lista para el informe."""
    print("| n | Comparaciones A | Comparaciones B | Comparaciones C "
          "| Tiempo A (s) | Tiempo B (s) | Tiempo C (s) |")
    print("| --- | --- | --- | --- | --- | --- | --- |")
    for indice, n in enumerate(TAMANOS):
        comps = [resultados[e]["comparaciones"][indice] for e in ESCENARIOS]
        tiempos = [resultados[e]["tiempos"][indice] for e in ESCENARIOS]
        print(f"| {n} | " + " | ".join(f"{c:,}" for c in comps) + " | "
              + " | ".join(f"{t:.6f}" for t in tiempos) + " |")
    print()


def imprimir_control_mejor_caso() -> None:
    """Contrasta el escenario B contra el mejor caso teorico del algoritmo.

    Con una entrada ya ordenada, insertion sort hace exactamente n - 1
    comparaciones. Sirve para mostrar cuanto se aleja de ese limite el
    escenario B, donde el 2% final si obliga a recorrer la parte ordenada.
    """
    print("Control: mejor caso teorico (entrada ya ordenada) vs. escenario B")
    print("| n | Comparaciones entrada ya ordenada | n - 1 | Comparaciones "
          "escenario B |")
    print("| --- | --- | --- | --- |")
    for n in TAMANOS:
        _, comp_ordenado = insertion_sort(generar_ordenado(n))
        _, comp_b = insertion_sort(generar_casi_ordenado(n, SEMILLA))
        print(f"| {n} | {comp_ordenado:,} | {n - 1:,} | {comp_b:,} |")
    print()


def main() -> None:
    """Corre la verificacion, el experimento, la tabla y las graficas."""
    verificar_correccion()
    resultados = ejecutar_experimento()
    imprimir_tabla(resultados)
    imprimir_control_mejor_caso()

    graficar(resultados, "comparaciones",
             "Insertion sort: comparaciones vs. tamano de entrada (Tamiza)",
             "Comparaciones entre elementos (conteo)",
             "parte3_comparaciones.png")
    graficar(resultados, "tiempos",
             "Insertion sort: tiempo de ejecucion vs. tamano de entrada "
             "(Tamiza)",
             "Tiempo de ejecucion (segundos)",
             "parte3_tiempo.png")


if __name__ == "__main__":
    main()
