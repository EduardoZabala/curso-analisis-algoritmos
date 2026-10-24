# Retroalimentación — Laboratorio 02: Dividir y vencer

**Estudiante:** Jhon Eduardo Zabala · **Laboratorio:** Laboratorio evaluativo 02 — Dividir y vencer
**Fecha límite:** 2026-10-21 23:59 · **Versión revisada:** commit `e3a9dec`

Excelente trabajo: entregó un laboratorio completo, riguroso y bien sustentado con sus propias mediciones.

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
- Identificó que divide y vencerás empieza a ganar desde n = 50 y explicó el porqué con el costo fijo de las llamadas recursivas.
- Comparó con el máximo de un arreglo: combinar cuesta una sola comparación, la recurrencia da Θ(n) y dividir no mejora nada.
- Recomendó divide y vencerás y declaró su estimación para 1.000.000 de registros como estimación, sin usar regla de tres.

## 2. Calidad de la explicación teórica (20 / 20)
**Lo que hizo bien:**
- Planteó T(n) = 2T(n/2) + Θ(n) explicando de dónde sale cada término.
- Verificó la condición del caso 2 del método maestro y llegó a Θ(n log n).
- Justificó el Θ(n²) de la fuerza bruta con la suma n + (n−1) + … + 1.

## 3. Corrección de la implementación (25 / 25)
**Lo que hizo bien:**
- Las tres funciones dan la suma correcta en todos los casos pedidos y coinciden en listas aleatorias.
- `subarreglo_maximo` resuelve los tres casos sin llamar a la fuerza bruta y ninguna función cambia la lista recibida.
- Tiene *type hints* y *docstrings* en todas las funciones. Sus pruebas son completas y revisan también los índices.

## 4. Calidad del análisis de las gráficas (25 / 25)
**Lo que hizo bien:**
- La gráfica tiene ambas curvas en los mismos ejes, título, ejes rotulados y leyenda, con 14 tamaños y una vista log-log.
- Calculó los factores al duplicar n (4.02 y 2.10 entre 4000 y 8000) y los contrastó con Θ(n²) y Θ(n log n).
- Lo que afirma coincide con lo que se ve en la gráfica (por ejemplo, unos 1400 ms contra unos 10 ms en n = 8000).
- Repitió las mediciones y usó la mediana.

## 5. Documentación y organización del informe (10 / 10)
**Lo que hizo bien:**
- La carpeta `lab2-divide-y-vencer/` está en la ubicación acordada y tiene todos los archivos del entregable.
- El informe sigue el orden pedido, enlaza el código en cada parte, incluye la gráfica visible y las instrucciones para reproducir.
- Hay cinco commits descriptivos del laboratorio.

## ¿El código funciona?
Sí. Las pruebas pasan, ambas soluciones dan siempre la misma suma y `medicion.py` corre sin errores y genera la gráfica.

## Para el próximo laboratorio
- Mantenga el hábito de repetir mediciones y reportar la mediana.
- Siga sustentando cada conclusión con datos propios, como lo hizo aquí.
- Conserve commits pequeños y con mensajes claros.
