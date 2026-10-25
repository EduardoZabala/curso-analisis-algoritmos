"""Pruebas de la lista enlazada y la tabla hash de guias.

Verifica busquedas exitosas e infructuosas, la colision forzada de las
guias 10, 24 y 17 con m = 7, el factor de carga y, en colecciones
aleatorias, que la lista y la tabla responden exactamente lo mismo.

Uso:
    python pruebas.py
"""

import random

from estructuras import ListaEnlazada, Nodo, TablaHash

SEMILLA = 2026
ESTADOS = ("en bodega", "en reparto", "entregado", "devuelto")


def longitud(lista: ListaEnlazada) -> int:
    """Cuenta los nodos siguiendo los enlaces, sin confiar en tamano."""
    contador = 0
    actual: Nodo | None = lista.cabeza
    while actual is not None:
        contador += 1
        actual = actual.siguiente
    return contador


# 1. Serie de ejemplo de la situacion problema en ambas estructuras.
EJEMPLO = [(1000000010, "en bodega"), (1000000024, "en reparto"),
           (1000000017, "en bodega"), (1000000005, "entregado")]
lista = ListaEnlazada()
tabla = TablaHash(7)
for guia, estado in EJEMPLO:
    lista.insertar(guia, estado)
    tabla.insertar(guia, estado)

for guia, estado in EJEMPLO:
    assert lista.buscar(guia) == estado, f"lista: guia {guia}"
    assert tabla.buscar(guia) == estado, f"tabla: guia {guia}"
assert lista.buscar(1000000099) is None, "lista: guia inexistente"
assert tabla.buscar(1000000099) is None, "tabla: guia inexistente"
assert lista.tamano == 4 and longitud(lista) == 4
assert tabla.tamano == 4
# La ultima insertada queda en la cabeza: insercion al inicio.
assert lista.cabeza is not None and lista.cabeza.guia == 1000000005
print("  OK  serie de ejemplo: 4 exitosas y 1 infructuosa en ambas")

# 2. Estructuras vacias: toda busqueda es infructuosa.
assert ListaEnlazada().buscar(10) is None
assert TablaHash(7).buscar(10) is None
assert TablaHash(7).factor_carga() == 0
print("  OK  estructuras vacias")

# 3. Colision forzada: con m = 7, 10, 24 y 17 caen en la casilla 3.
tabla = TablaHash(7)
for guia in (10, 24, 17):
    assert tabla.hash(guia) == 3, f"h({guia}) deberia ser 3"
    tabla.insertar(guia, "en bodega")
tabla.insertar(5, "entregado")  # h(5) = 5: otra casilla

for guia in (10, 24, 17):
    assert tabla.buscar(guia) == "en bodega", f"colision: guia {guia}"
assert tabla.buscar(5) == "entregado"
assert tabla.buscar(31) is None, "31 tambien va a la casilla 3 y no esta"
assert tabla.buscar(99) is None
assert longitud(tabla.casillas[3]) == 3, "la casilla 3 debe tener 3 guias"
assert tabla.casillas[3].tamano == 3
assert longitud(tabla.casillas[5]) == 1
otras = [i for i in range(7) if i not in (3, 5)]
assert all(tabla.casillas[i].cabeza is None for i in otras)
print("  OK  colision 10, 24, 17 en la casilla 3 (longitud 3)")

# 4. Factor de carga tras exactamente esas tres inserciones.
tabla = TablaHash(7)
for guia in (10, 24, 17):
    tabla.insertar(guia, "en bodega")
assert tabla.buscar(24) == "en bodega"
assert tabla.buscar(99) is None
assert tabla.factor_carga() == 3 / 7
print("  OK  factor de carga 3/7")

# 5. Colecciones aleatorias: lista y tabla responden lo mismo.
azar = random.Random(SEMILLA)
COLECCIONES = 50
for numero in range(COLECCIONES):
    n = azar.randint(1, 600)
    m = azar.choice((1, 2, 7, 13, 97, 101, 997))
    guias = azar.sample(range(10**9, 10**10), n)
    estados = {guia: azar.choice(ESTADOS) for guia in guias}
    lista, tabla = ListaEnlazada(), TablaHash(m)
    for guia in guias:
        lista.insertar(guia, estados[guia])
        tabla.insertar(guia, estados[guia])

    assert lista.tamano == tabla.tamano == n
    assert sum(longitud(c) for c in tabla.casillas) == n, (
        f"coleccion {numero}: se perdio o duplico alguna guia")
    assert tabla.factor_carga() == n / m
    for guia in guias:
        assert lista.buscar(guia) == tabla.buscar(guia) == estados[guia], (
            f"coleccion {numero}: guia existente {guia}")
    inexistentes = 0
    while inexistentes < 100:
        guia = azar.randint(10**9, 10**10 - 1)
        if guia in estados:
            continue
        assert lista.buscar(guia) is None and tabla.buscar(guia) is None, (
            f"coleccion {numero}: guia inexistente {guia}")
        inexistentes += 1
print(f"  OK  {COLECCIONES} colecciones aleatorias: lista y tabla coinciden")

print("\nTodas las pruebas pasaron.")
