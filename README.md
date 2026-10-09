# Curso de Análisis de Algoritmos

Repositorio para la entrega de laboratorios evaluativos, ejercicios de clase y
benchmarks desarrollados durante el semestre en la materia **Análisis de
Algoritmos**.

## Estructura del repositorio

El repositorio mantiene la siguiente organización de carpetas:

- `lab1-fundamentos-complejidad-recurrencias/`: Laboratorio evaluativo 01 —
  análisis de insertion sort y merge sort sobre el caso de la plataforma
  Tamiza (informe, código instrumentado y gráficas).
- `lab2-divide-y-vencer/`: Laboratorio evaluativo 02 — subarreglo máximo por
  fuerza bruta y por divide y vencerás sobre el caso de la cooperativa de
  tiendas (informe, pruebas, medición y gráfica).
- `laboratorios/`: contiene una carpeta por cada uno de los cinco informes de
  laboratorio evaluativos del semestre.
- `ejercicios-clase/`: código de las sesiones prácticas no evaluativas,
  incluyendo los ejercicios de Python de la Semana 2.
- `benchmarks/`: scripts compartidos de medición de tiempos y graficación,
  reutilizados en los laboratorios evaluativos.

## Entorno de trabajo

Las dependencias de Python se instalan en el entorno virtual de la raíz del
repositorio y están registradas en `requirements.txt`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Estructura del proyecto

```
curso-analisis-algoritmos/
├── lab1-fundamentos-complejidad-recurrencias/
│   ├── README.md
│   ├── algoritmos.py
│   ├── datos.py
│   ├── parte3_casos.py
│   ├── parte4_complejidad.py
│   └── graficas/
├── lab2-divide-y-vencer/
│   ├── README.md
│   ├── subarreglo.py
│   ├── pruebas.py
│   ├── medicion.py
│   └── graficas/
│       └── tiempo_vs_n.png
├── laboratorios/
├── ejercicios-clase/
├── benchmarks/
├── requirements.txt
├── README.md
└── .gitignore
```

## Cómo clonar el proyecto

Para obtener una copia local del repositorio, ejecute:

```bash
git clone https://github.com/EduardoZabala/curso-analisis-algoritmos.git
cd curso-analisis-algoritmos
```

## Autor

- **Nombre:** Jhon Eduardo Zabala Garzon
- **Correo:** jhonzabala329026@correo.itm.edu.co
- **Grupo de Análisis:** 190304006-1
