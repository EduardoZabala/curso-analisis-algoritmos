# Laboratorio evaluativo 03 — Estructuras de datos

**Autor:** Jhon Eduardo Zabala Garzon
**Correo:** jhonzabala329026@correo.itm.edu.co
**Grupo de Análisis:** 190304006-1
**Caso analizado:** Rutas del Caribe — consulta del estado de un envío por
número de guía (lista enlazada vs. tabla hash)

---

## Cómo reproducir el experimento

Todo el código se ejecuta con el entorno virtual de la raíz del repositorio,
que ya tiene `matplotlib` registrado en `requirements.txt`.

```bash
# 1. Clonar y entrar al repositorio
git clone https://github.com/EduardoZabala/curso-analisis-algoritmos.git
cd curso-analisis-algoritmos

# 2. Crear y activar el entorno virtual (si aún no existe)
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# 3. Instalar las dependencias registradas
pip install -r requirements.txt

# 4. Ejecutar las pruebas y la medición
cd lab3-estructuras-datos
python pruebas.py                  # Parte 1: casos con assert
python medicion.py                 # Parte 2: tablas + las dos gráficas + estimación
```

`pruebas.py` termina con `Todas las pruebas pasaron.`; si algún caso falla, se
detiene con un `AssertionError` que dice cuál. `medicion.py` tarda unos 10
segundos e imprime las tablas que aparecen en este informe. Las guías se
generan con semilla `42` y las inexistentes con semilla `7`, así que los datos
son idénticos en cualquier máquina; los tiempos cambian entre equipos, pero no
la forma de las curvas.

**Equipo donde se tomaron las mediciones de este informe:** Intel Core
i7-14700HX, 31 GB de RAM, Linux x86-64, CPython 3.14.7, matplotlib 3.10.6.

---

## Parte 1 — Implementar y verificar las dos estructuras

Código de esta parte: [`estructuras.py`](estructuras.py) (las dos clases) y
[`pruebas.py`](pruebas.py) (las pruebas).

- `ListaEnlazada.insertar` crea el nodo, lo apunta a la cabeza actual y lo
  vuelve la nueva cabeza: Θ(1), sin recorrer nada. `buscar` avanza con un
  `while` desde la cabeza y se detiene al encontrar la guía o al llegar a
  `None`.
- `TablaHash` tiene `m` casillas y cada una es una `ListaEnlazada`
  (encadenamiento). `hash` es `guia % m`; `insertar` y `buscar` calculan la
  casilla y delegan en su lista, de modo que solo recorren esa cadena.
  `factor_carga` devuelve `tamano / m`. No uso `dict`, `set` ni `hash()` de
  Python en ninguna de las dos clases.

**Cómo verifiqué.** Además de comparar respuestas, cuento los nodos de una
cadena siguiendo los enlaces (función `longitud`), para no confiar solo en el
contador `tamano` que mantiene el propio código.

| Caso | Qué se comprueba |
| --- | --- |
| Serie de ejemplo del enunciado (4 guías) | Las 4 se encuentran con su estado en lista y tabla; `1000000099` da `None` en ambas; la última insertada queda en la cabeza |
| Estructuras vacías | Toda búsqueda da `None` y el factor de carga es 0 |
| Colisión forzada, m = 7 | `hash` de 10, 24 y 17 es 3; las tres se encuentran; la cadena de la casilla 3 tiene longitud 3; 31 (también va a la 3) da `None`; las demás casillas quedan vacías salvo la 5 |
| Factor de carga | Exactamente `3 / 7` tras insertar 10, 24 y 17 |
| 50 colecciones aleatorias | n entre 1 y 600, m ∈ {1, 2, 7, 13, 97, 101, 997}, semilla 2026: para **todas** las guías existentes lista, tabla y estado esperado coinciden; para 100 guías inexistentes por colección ambas dan `None`; la suma de longitudes de las cadenas es n |

El caso m = 1 es a propósito: toda la tabla queda en una sola cadena, el peor
caso posible, y aun así debe responder igual que la lista.

---

## Parte 2 — Medir y graficar

Código de esta parte: [`medicion.py`](medicion.py).

**Cómo medí.**

- **Experimento A:** 10 valores de n en una cadena donde n se duplica
  (100, 200, 400, 800, …, 25.600, 51.200): cuatro menores de 1.000 y dos
  mayores de 20.000. Para cada n la tabla usa el **primo más cercano a n/2**
  (columna m), así α queda en 2.00 (2.13 en n = 100, donde los primos están
  más espaciados en proporción).
- **Experimento B:** n = 20.000 fijo y m = primo más cercano a n/α para
  α ∈ {0,25; 0,5; 1; 2; 4; 6; 8; 10}.
- Las guías son enteros distintos de diez dígitos (`random.sample`, semilla
  42). Lista y tabla se construyen con **las mismas guías** y la construcción
  queda fuera del reloj.
- Antes de medir, el script verifica en cada n (y en cada α) que 200 guías
  existentes devuelven el mismo estado en lista y tabla, y que las 200
  inexistentes dan `None` en ambas; si no, se detiene.
- Cronometro con `time.perf_counter()` **solo** el ciclo de 200 búsquedas de
  guías inexistentes (generadas con `generar_guias_inexistentes`) y divido por
  200. El recolector de basura se apaga durante la tanda.
- **Repetí cada tanda 15 veces y reporto la mediana**, como en el laboratorio
  anterior.

![Tiempo medio por búsqueda de una guía inexistente vs. n: lista enlazada y tabla hash, en escala lineal y log-log](graficas/lista_vs_tabla.png)

En escala lineal la tabla queda pegada al eje; el panel log-log permite leerla.

| n | m | α | Lista (µs) | Tabla (µs) | Lista / Tabla |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 100 | 47 | 2.13 | 2.367 | 0.161 | 15 |
| 200 | 101 | 1.98 | 4.750 | 0.149 | 32 |
| 400 | 199 | 2.01 | 9.497 | 0.161 | 59 |
| 800 | 401 | 2.00 | 18.950 | 0.165 | 115 |
| 1600 | 797 | 2.01 | 37.267 | 0.168 | 222 |
| 3200 | 1601 | 2.00 | 74.895 | 0.165 | 453 |
| 6400 | 3203 | 2.00 | 149.804 | 0.176 | 851 |
| 12800 | 6397 | 2.00 | 298.451 | 0.167 | 1,787 |
| 25600 | 12799 | 2.00 | 596.591 | 0.168 | 3,548 |
| 51200 | 25601 | 2.00 | 1188.125 | 0.172 | 6,906 |

Factor por el que se multiplica el tiempo cuando n se duplica:

| n → 2n | Lista | Esperado Θ(n) | Tabla | Esperado Θ(1) |
| --- | ---: | ---: | ---: | ---: |
| 100 → 200 | 2.01 | 2.00 | 0.92 | 1.00 |
| 200 → 400 | 2.00 | 2.00 | 1.08 | 1.00 |
| 400 → 800 | 2.00 | 2.00 | 1.03 | 1.00 |
| 800 → 1600 | 1.97 | 2.00 | 1.02 | 1.00 |
| 1600 → 3200 | 2.01 | 2.00 | 0.98 | 1.00 |
| 3200 → 6400 | 2.00 | 2.00 | 1.06 | 1.00 |
| 6400 → 12800 | 1.99 | 2.00 | 0.95 | 1.00 |
| 12800 → 25600 | 2.00 | 2.00 | 1.01 | 1.00 |
| 25600 → 51200 | 1.99 | 2.00 | 1.02 | 1.00 |

![Tiempo medio por búsqueda de una guía inexistente vs. factor de carga, con n = 20.000 y ajuste lineal](graficas/tiempo_vs_alfa.png)

La columna "cadena recorrida" es la longitud media de la cadena que revisó
cada búsqueda infructuosa, es decir, cuántas guías comparó.

| α objetivo | m | α real | Cadena recorrida | Tabla (µs) |
| ---: | ---: | ---: | ---: | ---: |
| 0.25 | 79999 | 0.250 | 0.21 | 0.093 |
| 0.5 | 40009 | 0.500 | 0.52 | 0.109 |
| 1 | 19997 | 1.000 | 0.93 | 0.123 |
| 2 | 10007 | 1.999 | 2.10 | 0.168 |
| 4 | 4999 | 4.001 | 4.00 | 0.202 |
| 6 | 3331 | 6.004 | 6.12 | 0.292 |
| 8 | 2503 | 7.990 | 8.04 | 0.334 |
| 10 | 1999 | 10.005 | 9.66 | 0.374 |

Ajuste por mínimos cuadrados: **tiempo ≈ 0,096 + 0,029·α µs**.

---

## Parte 3 — Análisis

### 1. Costo teórico

En la lista, una guía que no existe obliga a compararla con cada uno de los n
nodos, porque solo al llegar a `None` se sabe que no está. No hay atajo: son
exactamente n comparaciones, Θ(n).

En la tabla, buscar tiene dos pasos: calcular `guia % m` (Θ(1)) y recorrer la
cadena de esa casilla. Si cada guía cae en cualquier casilla con la misma
probabilidad, sin depender de las demás (**hash uniforme simple**), las n
guías se reparten en m cadenas y la cadena esperada mide n/m = α. Total:
Θ(1 + α). Si m crece con n, α no crece y la búsqueda es Θ(1) esperado.

Si todas las guías cayeran en la misma casilla, esa cadena sería la lista
original con un paso extra: Θ(n) (por ejemplo, m = 1000 y guías que
terminan todas en `000`).

### 2. Lo medido contra lo esperado

En la primera gráfica, de n = 25.600 a n = 51.200 la lista pasó de 596,6 a
1188,1 µs: se multiplicó por **1,99**, lo que Θ(n) predice (2). La tabla pasó
de 0,168 a 0,172 µs: **1,02**, prácticamente constante, como Θ(1). Toda la
cadena de duplicaciones da 1,97–2,01 para la lista y 0,92–1,08 para la tabla.
En log-log la lista es una recta de pendiente 1 y la tabla una horizontal.

En la segunda, el tiempo sube de 0,093 µs (α = 0,25) a 0,374 µs (α = 10) y
los puntos caen cerca de una recta: es la forma a + b·α de Θ(1 + α). La recta
no parte de cero: `a` = 0,096 µs es el costo fijo (llamada, módulo, acceso a
la casilla) y cada guía de la cadena suma `b` = 0,029 µs. La columna
"cadena recorrida" confirma el supuesto: con guías aleatorias la cadena mide
casi exactamente α.

### 3. Explique las colisiones

Una colisión ocurre cuando dos guías distintas dan la misma casilla. Es
inevitable porque hay unos 9·10⁹ números de guía posibles y solo m casillas:
muchas comparten residuo. Aunque m supere a n, dos guías concretas pueden
coincidir: en mi medición con α = 0,25 la cadena visitada promedió 0,21, no 0.

Con m = 7: 10 = 7·1 + 3, 24 = 7·3 + 3 y 17 = 7·2 + 3; las tres van a la 3.

- **Encadenamiento** (mi implementación): la casilla 3 guarda una lista
  17 → 24 → 10. Ventaja: nunca se llena y borrar es sencillo. Costo: memoria
  para los enlaces y saltos por punteros; si α crece, la cadena se alarga.
- **Direccionamiento abierto** (sondeo lineal): 10 ocupa la 3, 24 prueba 3 y
  queda en 4, 17 prueba 3 y 4 y queda en 5. Ventaja: todo vive en un arreglo,
  sin punteros. Costo: α no puede pasar de 1, las rachas ocupadas crecen
  (una guía que caiga en 4 ahora va a la 6) y al borrar hay que dejar lápidas.

### 4. Tabla hash o árbol de búsqueda

La tabla no sirve para "guías entre X y Y": `guia % m` desordena a propósito
las guías, y guías consecutivas quedan en casillas lejanas. La única forma es
revisar las n guías, Θ(n), en cada consulta.

Un BST guarda las guías ordenadas: se baja hasta X en Θ(h) y desde ahí el
recorrido en orden entrega las k guías del rango, Θ(h + k).

Pero si las 400.000 guías llegan ordenadas, cada una es mayor que todas las
anteriores y se cuelga a la derecha de la última: el árbol es una fila de
altura **h = n − 1 = 399.999**. Insertar la i-ésima cuesta i − 1
comparaciones; en total n(n−1)/2 ≈ **8·10¹⁰**. Con mi costo de unos 23 ns por
nodo recorrido serían unos 30 minutos solo en construirlo, y cada consulta de
rango costaría Θ(n). Equilibrado, h ≈ log₂ 400.000 ≈ **18** y la construcción
cuesta n·log₂ n ≈ **7,4·10⁶** comparaciones, unas 10.000 veces menos.

### 5. Concepto para la jefa de operaciones

Recomiendo **combinar**, sobre los mismos envíos, una **tabla hash** para el
call center y un **árbol de búsqueda balanceado** (AVL o rojo-negro, no un BST
simple, porque las guías llegan en orden) para el monitoreo por rango.

*Estimación, no medición*, para 5.000.000 de envíos y una guía inexistente:

| Estructura | Modelo | Tiempo por búsqueda |
| --- | --- | ---: |
| Lista enlazada | 23,2 ns × n | ≈ **116 ms** |
| Tabla hash (α ≈ 2) | constante | ≈ **0,17 µs** |

Razonamiento: la lista dobla su tiempo cada vez que n se duplica, así que es
una recta que pasa por el origen; ajusté su pendiente con los cuatro n más
grandes (23,2 ns por nodo) y la evalué en 5·10⁶. La tabla no creció con n
mientras α se mantuvo en 2, así que su estimación es lo medido, siempre que m
crezca a un primo cercano a 2.500.000. 1.000 consultas costarían casi 2 minutos en la
lista y menos de un milisegundo en la tabla. Supuestos: mismo equipo y Python; con 5 millones de nodos la memoria caché
ayudaría menos, así que la lista podría tardar incluso más.
