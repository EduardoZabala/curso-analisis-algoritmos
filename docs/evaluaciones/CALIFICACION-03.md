# Retroalimentación — Laboratorio 03: Estructuras de datos

**Estudiante:** Jhon Eduardo Zabala · **Laboratorio:** Laboratorio evaluativo 03 — Estructuras de datos
**Fecha límite:** 2026-11-01 23:59 · **Versión revisada:** commit `17ef45a`

Excelente trabajo: un laboratorio completo, preciso y bien sustentado con sus propias mediciones.

## Nota

| Criterio | Puntos |
|---|---|
| Corrección conceptual | 20 / 20 |
| Calidad de la explicación teórica | 20 / 20 |
| Corrección de la implementación | 25 / 25 |
| Calidad del análisis de las gráficas | 25 / 25 |
| Documentación y organización del informe | 10 / 10 |
| **Total** | **100 / 100** |
| **Nota (0–5)** | **5.00** |

## 1. Corrección conceptual (20 / 20)
**Lo que hizo bien:**
- Explica la colisión con el ejemplo de 10, 24 y 17 en `m = 7` y compara encadenamiento y direccionamiento abierto, con ventajas y costos de cada uno.
- Justifica con claridad por qué la tabla no sirve para rangos y qué ofrece el árbol de búsqueda.
- Estima la altura y las comparaciones del árbol degenerado frente al equilibrado, con números.
- Recomienda las dos estructuras juntas, declara la estimación a 5.000.000 de envíos como estimación y explica de dónde sale la cifra, sin una regla de tres a ciegas.

## 2. Calidad de la explicación teórica (20 / 20)
**Lo que hizo bien:**
- Justifica el Θ(n) de la lista y el Θ(1 + α) de la tabla.
- Nombra el supuesto de hash uniforme simple y explica qué pasa si todas las guías caen en una casilla, apoyándolo con su caso de control con `m = 1`.

## 3. Corrección de la implementación (25 / 25)
**Lo que hizo bien:**
- Lista y tabla devuelven el estado correcto en búsquedas exitosas e infructuosas; la colisión forzada con `m = 7` y `factor_carga` funcionan.
- La tabla reutiliza la lista, sin `dict`, `set` ni `hash()`, y `buscar` usa un ciclo `while`.
- Sus pruebas cubren más de lo pedido (50 colecciones aleatorias) y todas pasan.
- Docstrings con `Args` y `Returns`, type hints y separación correcta entre funciones.

## 4. Calidad del análisis de las gráficas (25 / 25)
**Lo que hizo bien:**
- Ambas gráficas tienen título, ejes rotulados y leyenda; la primera cubre 10 valores de `n` y la segunda 8 valores de α.
- Calcula los factores de crecimiento en todas las duplicaciones y los contrasta con Θ(n) y Θ(1); la lectura de la segunda gráfica es coherente con Θ(1 + α).
- Las cifras del informe coinciden con lo que muestran las imágenes publicadas.

## 5. Documentación y organización del informe (10 / 10)
**Lo que hizo bien:**
- Estructura de carpetas exacta del entregable, README en el orden pedido y gráficas visibles con ruta relativa.
- Cada parte práctica enlaza su código, hay instrucciones de reproducción y varios commits descriptivos del laboratorio.

## ¿El código funciona?
Sí. Las pruebas pasan completas y la medición corre y genera las dos gráficas sin errores.
