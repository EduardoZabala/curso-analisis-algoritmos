# Retroalimentación — Laboratorio 01: Fundamentos, complejidad y recurrencias

**Estudiante:** Jhon Eduardo Zabala Garzon · **Laboratorio:** Laboratorio evaluativo 01 — Fundamentos, complejidad y recurrencias
**Fecha límite:** 2026-10-06 23:59 · **Versión revisada:** commit `22f2f85`

Excelente trabajo: un informe completo, con datos propios y muy bien sustentado.

## Nota

| Criterio | Puntos |
|---|---|
| Corrección conceptual | 24 / 25 |
| Calidad de la explicación teórica | 25 / 25 |
| Corrección de la implementación | 20 / 20 |
| Calidad del análisis de las gráficas | 19 / 20 |
| Documentación y organización del informe | 6 / 10 |
| **Total** | **94 / 100** |
| **Nota (0–5)** | **4.70** |

## 1. Corrección conceptual (24 / 25)
**Lo que hizo bien:**
- Distingue bien entre que el algoritmo sea correcto y que sea viable, y nombra la restricción que se incumple: la ventana de 4 horas.
- Explica con sus propias mediciones por qué duplicar la velocidad del servidor no alcanza (el escenario C seguiría pasándose de la ventana).
- Su segundo ejemplo (el validador de duplicados con 45.000 filas) tiene datos y una restricción clara.
- En la parte ambiental traduce las horas de proceso a kWh por año y a varios años.
- En la parte ética da dos perjuicios concretos (el paciente y el operador del centro de contacto), dice quién asume el costo y discute muy bien la obligación que impone el orden de la lista.

**Lo que puede mejorar:**
- En la parte ambiental el consumo se basa en un supuesto de 450 W; está bien declarado, pero podría mencionar de dónde sale esa cifra.

## 2. Calidad de la explicación teórica (25 / 25)
**Lo que hizo bien:**
- Define peor caso, mejor caso y caso promedio indicando sobre qué se toma cada uno y justifica por qué usaría el peor caso para decidir.
- Dejó la predicción antes del experimento y, cuando falló en el escenario B, lo reconoció y lo explicó con una medición de control.
- Plantea la recurrencia de merge sort explicando cada término, la resuelve con el método maestro verificando los tres casos y la confirma con el árbol de recursión.
- El análisis línea a línea de insertion sort y la tabla de complejidades son completos.

## 3. Corrección de la implementación (20 / 20)
**Lo que hizo bien:**
- Ambos algoritmos ordenan bien en los tres escenarios, no cambian la lista recibida y cuentan solo comparaciones entre elementos.
- No usa `sorted()` ni `list.sort()`, y la mezcla de merge sort es propia y recursiva.
- Los generadores respetan el tamaño, valores distintos y semilla reproducible.
- El código sigue PEP 8 y todas las funciones tienen tipos y descripción.

## 4. Calidad del análisis de las gráficas (19 / 20)
**Lo que hizo bien:**
- Las tres gráficas tienen título, ejes con unidades y leyenda, y muestran las curvas pedidas en los mismos ejes.
- Identifica con evidencia el peor caso (C), el caso promedio (A) y explica por qué B no es el mejor caso.
- Concluye con la gráfica que merge sort conviene, describe cada curva y explica el comportamiento con tamaños pequeños.
- El concepto técnico recomienda un algoritmo, responde sobre el servidor con un dato medido, declara la extrapolación como estimación y discute memoria y estabilidad.

**Lo que puede mejorar:**
- Para los dos tamaños más grandes midió una sola vez; repetir la medición habría dado curvas más estables.

## 5. Documentación y organización del informe (6 / 10)
**Lo que hizo bien:**
- La carpeta del laboratorio, los archivos y las gráficas están donde se pedía.
- El informe sigue el orden pedido, tiene instrucciones para reproducir, las gráficas se ven y cada parte enlaza su código.

**Lo que puede mejorar:**
- Solo hay un commit que contiene el laboratorio completo. Se pedían al menos cinco commits descriptivos que muestren el avance. Haga commits pequeños y frecuentes, por ejemplo uno por cada parte.

## ¿El código funciona?
Sí. Los scripts corren sin errores, los algoritmos ordenan bien (probé con listas aleatorias y con casos pequeños) y las gráficas se generan.

## Para el próximo laboratorio
- Haga commits frecuentes, uno por cada avance importante, con mensajes que digan qué se hizo.
- Repita las mediciones largas varias veces y use el promedio o la mediana.
- Indique de dónde salen los supuestos numéricos (como la potencia del servidor).
- Mantenga el nivel de verificación con casos de control, como hizo con el mejor caso.
