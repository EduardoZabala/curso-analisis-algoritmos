"""Parte 2 - Medicion del tiempo de busqueda en la lista y en la tabla hash.

Experimento A: mide la busqueda de guias inexistentes en la lista enlazada
y en la tabla hash (alfa cercano a 2) para varios n, y genera
graficas/lista_vs_tabla.png.

Experimento B: con n fijo, mide la misma busqueda en tablas con distinto
numero de casillas m, para varios factores de carga, y genera
graficas/tiempo_vs_alfa.png.

Imprime las tablas del informe, los factores de crecimiento al duplicar n
y la estimacion para 5.000.000 de envios.

Uso:
    python medicion.py
"""

import gc
import random
import statistics
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # backend sin ventana: debe fijarse antes de importar
# pyplot, por eso los imports siguientes no van al inicio del archivo.
import matplotlib.pyplot as plt  # noqa: E402

from estructuras import ListaEnlazada, TablaHash  # noqa: E402

Estructura = ListaEnlazada | TablaHash

# Cadena donde n se duplica en cada paso: dos valores menores de 1.000 (100
# y 200, ademas de 400 y 800) y dos mayores de 20.000 (25.600 y 51.200).
TAMANOS = [100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600, 51200]
ALFA_OBJETIVO_A = 2
N_FIJO_B = 20_000
ALFAS_B = [0.25, 0.5, 1, 2, 4, 6, 8, 10]
BUSQUEDAS = 200
MUESTRA_VERIFICACION = 200
REPETICIONES = 15
SEMILLA = 42
ESTADOS = ("en bodega", "en reparto", "entregado", "devuelto")
ENVIOS_OBJETIVO = 5_000_000
CARPETA_GRAFICAS = Path(__file__).parent / "graficas"
COLORES = {"Lista enlazada": "#eb6834", "Tabla hash": "#2a78d6"}
MARCADORES = {"Lista enlazada": "o", "Tabla hash": "s"}


def generar_guias_inexistentes(
    existentes: set[int], cantidad: int, semilla: int = 7
) -> list[int]:
    """Genera guias de diez digitos que no estan en la coleccion.

    Args:
        existentes: guias almacenadas en las estructuras.
        cantidad: cuantas guias inexistentes generar.
        semilla: semilla del generador, para reproducir la medicion.

    Returns:
        Una lista con `cantidad` guias que no pertenecen a `existentes`.
    """
    azar = random.Random(semilla)
    inexistentes: list[int] = []
    while len(inexistentes) < cantidad:
        guia = azar.randint(10**9, 10**10 - 1)
        if guia not in existentes:
            inexistentes.append(guia)
    return inexistentes


def generar_envios(n: int) -> list[tuple[int, str]]:
    """Genera n envios reproducibles con guias distintas de diez digitos.

    Args:
        n: numero de envios.

    Returns:
        Lista de pares (guia, estado). Con la misma semilla y el mismo n la
        lista es siempre la misma.
    """
    azar = random.Random(SEMILLA)
    guias = azar.sample(range(10**9, 10**10), n)
    return [(guia, azar.choice(ESTADOS)) for guia in guias]


def es_primo(numero: int) -> bool:
    """Indica si un entero es primo, probando divisores hasta su raiz.

    Args:
        numero: entero a revisar.

    Returns:
        True si es primo.
    """
    if numero < 2:
        return False
    divisor = 2
    while divisor * divisor <= numero:
        if numero % divisor == 0:
            return False
        divisor += 1
    return True


def primo_cercano(objetivo: float) -> int:
    """Busca el primo mas cercano a un valor, alejandose hacia ambos lados.

    Args:
        objetivo: valor alrededor del cual se busca.

    Returns:
        El primo mas cercano (si hay empate, el menor).
    """
    base = max(2, round(objetivo))
    distancia = 0
    while True:
        for candidato in (base - distancia, base + distancia):
            if es_primo(candidato):
                return candidato
        distancia += 1


def construir(envios: list[tuple[int, str]], m: int | None) -> Estructura:
    """Construye una lista (m = None) o una tabla de m casillas.

    Args:
        envios: pares (guia, estado) a insertar.
        m: numero de casillas, o None para una lista enlazada.

    Returns:
        La estructura con todos los envios insertados.
    """
    estructura: Estructura = ListaEnlazada() if m is None else TablaHash(m)
    for guia, estado in envios:
        estructura.insertar(guia, estado)
    return estructura


def cronometrar(estructura: Estructura, guias: list[int]) -> float:
    """Mide el tiempo medio por busqueda de una tanda de guias.

    Solo las busquedas quedan dentro del reloj. El recolector de basura se
    apaga durante la tanda para que sus pausas no se sumen.

    Args:
        estructura: lista o tabla ya construida.
        guias: guias a buscar, ya generadas.

    Returns:
        Tiempo medio por busqueda, en segundos.
    """
    buscar = estructura.buscar
    gc.disable()
    try:
        inicio = time.perf_counter()
        for guia in guias:
            buscar(guia)
        fin = time.perf_counter()
    finally:
        gc.enable()
    return (fin - inicio) / len(guias)


def mediana_de(estructura: Estructura, guias: list[int]) -> float:
    """Repite la tanda REPETICIONES veces y devuelve la mediana.

    Args:
        estructura: lista o tabla ya construida.
        guias: guias a buscar.

    Returns:
        Mediana del tiempo medio por busqueda, en segundos.
    """
    return statistics.median(cronometrar(estructura, guias)
                             for _ in range(REPETICIONES))


def verificar(envios: list[tuple[int, str]], inexistentes: list[int],
              lista: ListaEnlazada, tabla: TablaHash) -> None:
    """Comprueba que lista y tabla responden lo mismo antes de medir.

    Revisa una muestra de guias existentes (deben dar su estado en ambas)
    y las guias inexistentes de la medicion (deben dar None en ambas).

    Raises:
        AssertionError: si alguna respuesta no coincide.
    """
    muestra = random.Random(SEMILLA).sample(
        envios, min(MUESTRA_VERIFICACION, len(envios)))
    for guia, estado in muestra:
        assert lista.buscar(guia) == tabla.buscar(guia) == estado, (
            f"guia {guia}: lista y tabla no coinciden")
    for guia in inexistentes:
        assert lista.buscar(guia) is None and tabla.buscar(guia) is None, (
            f"guia inexistente {guia} encontrada")


def longitud_media_recorrida(tabla: TablaHash, guias: list[int]) -> float:
    """Promedia la longitud de las cadenas que recorre cada busqueda.

    Para una guia inexistente la busqueda compara contra toda la cadena de
    su casilla, asi que esta longitud es el numero de comparaciones.

    Args:
        tabla: tabla ya construida.
        guias: guias buscadas en la medicion.

    Returns:
        Longitud media de las cadenas visitadas.
    """
    return statistics.mean(tabla.casillas[tabla.hash(g)].tamano
                           for g in guias)


def experimento_a() -> dict[str, list[float]]:
    """Mide lista y tabla (alfa cercano a 2) para cada n de TAMANOS.

    Returns:
        Diccionario estructura -> medianas en segundos, alineadas con
        TAMANOS, y "alfa" -> factor de carga real de cada tabla.
    """
    resultados: dict[str, list[float]] = {
        "Lista enlazada": [], "Tabla hash": [], "alfa": []}
    print("Experimento A: lista enlazada vs. tabla hash")
    print("| n | m | alfa | Lista (us) | Tabla (us) | Lista / Tabla |")
    print("| ---: | ---: | ---: | ---: | ---: | ---: |")
    for n in TAMANOS:
        envios = generar_envios(n)
        inexistentes = generar_guias_inexistentes(
            {guia for guia, _ in envios}, BUSQUEDAS)
        m = primo_cercano(n / ALFA_OBJETIVO_A)
        lista = construir(envios, None)
        tabla = construir(envios, m)
        verificar(envios, inexistentes, lista, tabla)

        t_lista = mediana_de(lista, inexistentes)
        t_tabla = mediana_de(tabla, inexistentes)
        resultados["Lista enlazada"].append(t_lista)
        resultados["Tabla hash"].append(t_tabla)
        resultados["alfa"].append(tabla.factor_carga())
        print(f"| {n} | {m} | {tabla.factor_carga():.2f} "
              f"| {t_lista * 1e6:.3f} | {t_tabla * 1e6:.3f} "
              f"| {t_lista / t_tabla:,.0f} |")
    print("Verificacion: lista y tabla coinciden en todos los n\n")
    return resultados


def experimento_b() -> tuple[list[float], list[float], list[float]]:
    """Mide la tabla con N_FIJO_B guias para cada alfa de ALFAS_B.

    Returns:
        Tres listas alineadas: alfa real de cada tabla, mediana del tiempo
        por busqueda (segundos) y longitud media de cadena recorrida.
    """
    envios = generar_envios(N_FIJO_B)
    inexistentes = generar_guias_inexistentes(
        {guia for guia, _ in envios}, BUSQUEDAS)
    lista = construir(envios, None)
    alfas, tiempos, cadenas = [], [], []
    print(f"Experimento B: efecto del factor de carga (n = {N_FIJO_B:,})")
    print("| alfa objetivo | m | alfa real | Cadena recorrida "
          "| Tabla (us) |")
    print("| ---: | ---: | ---: | ---: | ---: |")
    for alfa in ALFAS_B:
        m = primo_cercano(N_FIJO_B / alfa)
        tabla = construir(envios, m)
        verificar(envios, inexistentes, lista, tabla)
        tiempo = mediana_de(tabla, inexistentes)
        cadena = longitud_media_recorrida(tabla, inexistentes)
        alfas.append(tabla.factor_carga())
        tiempos.append(tiempo)
        cadenas.append(cadena)
        print(f"| {alfa} | {m} | {tabla.factor_carga():.3f} "
              f"| {cadena:.2f} | {tiempo * 1e6:.3f} |")
    print()
    return alfas, tiempos, cadenas


def ajuste_lineal(x: list[float], y: list[float]) -> tuple[float, float]:
    """Ajusta y = a + b * x por minimos cuadrados.

    Returns:
        La pareja (a, b).
    """
    pendiente, intercepto = statistics.linear_regression(x, y)
    return intercepto, pendiente


def imprimir_factores(resultados: dict[str, list[float]]) -> None:
    """Imprime cuanto se multiplica el tiempo cada vez que n se duplica."""
    print("| n -> 2n | Lista | Esperado Theta(n) | Tabla "
          "| Esperado Theta(1) |")
    print("| --- | ---: | ---: | ---: | ---: |")
    for i in range(len(TAMANOS) - 1):
        f_lista = (resultados["Lista enlazada"][i + 1]
                   / resultados["Lista enlazada"][i])
        f_tabla = resultados["Tabla hash"][i + 1] / resultados["Tabla hash"][i]
        print(f"| {TAMANOS[i]} -> {TAMANOS[i + 1]} | {f_lista:.2f} | 2.00 "
              f"| {f_tabla:.2f} | 1.00 |")
    print()


def graficar_a(resultados: dict[str, list[float]]) -> None:
    """Dibuja tiempo por busqueda vs. n, escala lineal y log-log.

    Args:
        resultados: salida de experimento_a().
    """
    CARPETA_GRAFICAS.mkdir(exist_ok=True)
    figura, ejes = plt.subplots(1, 2, figsize=(13, 5.5))
    for eje, escala in zip(ejes, ("lineal", "log-log")):
        for nombre in ("Lista enlazada", "Tabla hash"):
            microsegundos = [t * 1e6 for t in resultados[nombre]]
            eje.plot(TAMANOS, microsegundos, marker=MARCADORES[nombre],
                     markersize=6, linewidth=2, color=COLORES[nombre],
                     label=nombre)
        if escala == "log-log":
            eje.set_xscale("log")
            eje.set_yscale("log")
        eje.set_title(f"Escala {escala}")
        eje.set_xlabel("Numero de guias almacenadas n")
        eje.set_ylabel("Tiempo medio por busqueda (microsegundos, mediana)")
        eje.legend()
        eje.grid(True, which="both", linestyle=":", alpha=0.5)
    figura.suptitle("Busqueda de guias inexistentes: lista enlazada vs. "
                    f"tabla hash (alfa ~ {ALFA_OBJETIVO_A}, "
                    f"{BUSQUEDAS} busquedas, mediana de {REPETICIONES})")
    figura.tight_layout()
    figura.savefig(CARPETA_GRAFICAS / "lista_vs_tabla.png", dpi=150)
    plt.close(figura)
    print("Grafica escrita: graficas/lista_vs_tabla.png\n")


def graficar_b(alfas: list[float], tiempos: list[float]) -> None:
    """Dibuja tiempo por busqueda vs. alfa con su ajuste lineal a + b*alfa.

    Args:
        alfas: factor de carga real de cada tabla.
        tiempos: mediana del tiempo por busqueda en segundos.
    """
    CARPETA_GRAFICAS.mkdir(exist_ok=True)
    microsegundos = [t * 1e6 for t in tiempos]
    a, b = ajuste_lineal(alfas, microsegundos)
    figura, eje = plt.subplots(figsize=(8, 5.5))
    eje.plot(alfas, microsegundos, marker="s", markersize=7, linewidth=0,
             color=COLORES["Tabla hash"], label="Tabla hash (medido)")
    extremos = [0, max(alfas)]
    eje.plot(extremos, [a + b * x for x in extremos], linestyle="--",
             color="#555555",
             label=f"Ajuste a + b*alfa (a = {a:.3f} us, b = {b:.3f} us)")
    eje.set_title("Tiempo de busqueda infructuosa vs. factor de carga\n"
                  f"(tabla hash con n = {N_FIJO_B:,} guias, {BUSQUEDAS} "
                  f"busquedas, mediana de {REPETICIONES})")
    eje.set_xlabel("Factor de carga alfa = n / m (guias por casilla)")
    eje.set_ylabel("Tiempo medio por busqueda (microsegundos, mediana)")
    eje.set_xlim(left=0)
    eje.set_ylim(bottom=0)
    eje.legend()
    eje.grid(True, linestyle=":", alpha=0.5)
    figura.tight_layout()
    figura.savefig(CARPETA_GRAFICAS / "tiempo_vs_alfa.png", dpi=150)
    plt.close(figura)
    print(f"Ajuste tiempo = {a:.4f} + {b:.4f} * alfa (us)")
    print("Grafica escrita: graficas/tiempo_vs_alfa.png\n")


def estimar(resultados: dict[str, list[float]]) -> None:
    """Estima la busqueda infructuosa con ENVIOS_OBJETIVO guias.

    Lista: ajusta t = c * n por minimos cuadrados con los cuatro n mas
    grandes, donde la grafica ya es una recta. Tabla: con alfa fijo cerca
    de 2 el tiempo no depende de n, asi que se usa la mediana de lo medido
    en los n grandes. Es una estimacion, no una medicion.
    """
    grandes = slice(-4, None)
    xs, ys = TAMANOS[grandes], resultados["Lista enlazada"][grandes]
    c_lista = sum(x * y for x, y in zip(xs, ys)) / sum(x * x for x in xs)
    t_tabla = statistics.median(resultados["Tabla hash"][grandes])
    n = ENVIOS_OBJETIVO
    est_lista = c_lista * n
    print(f"Estimacion para {n:,} envios (busqueda de guia inexistente):")
    print(f"  lista: c = {c_lista * 1e9:.2f} ns por nodo -> "
          f"{est_lista * 1e3:,.1f} ms por busqueda")
    print(f"  tabla (alfa ~ 2): {t_tabla * 1e6:.3f} us por busqueda")
    print(f"  razon: {est_lista / t_tabla:,.0f} veces")
    print(f"  1.000 consultas en hora pico: lista {1000 * est_lista:,.0f} s, "
          f"tabla {1000 * t_tabla * 1e3:.2f} ms")


def main() -> None:
    """Corre ambos experimentos, las graficas y la estimacion."""
    resultados = experimento_a()
    imprimir_factores(resultados)
    graficar_a(resultados)
    alfas, tiempos, _ = experimento_b()
    graficar_b(alfas, tiempos)
    estimar(resultados)


if __name__ == "__main__":
    main()
