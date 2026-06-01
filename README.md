# Calculadora de Integrales: Regla de Simpson 1/3
Aplicación de escritorio nativa en Python diseñada para resolver integrales definidas utilizando la **Regla de Simpson 1/3**.

## Generalidades
* **Comparativa de Métodos:** El usuario puede evaluar integrales usando tanto la versión simple (1 solo segmento) como la compuesta ($n$ segmentos) en paralelo.
* **Motor Matemático Seguro (Sandbox):** El usuario escribe funciones libremente como texto (ej. `x**3 + 2*x - 5` o `exp(-x) * cos(x)`). La aplicación crea un entorno aislado con una lista blanca de NumPy para evitar inyecciones de código.
* **Geometría del Error:** Matplotlib embebido en la interfaz gráfica. Se dibujan las *parábolas exactas* que el algoritmo utiliza para aproximar el área, simplificando la comprensión de la reducción del error de truncamiento con más intervalos.

## Tecnologías Utilizadas
* **Python 3.x** Lenguaje de programación.
* **NumPy:** Para cálculos vectorizados.
* **Matplotlib:** Para el motor de graficación y renderizado de los polígonos.
* **CustomTkinter:** Para el diseño de la interfaz.

## Cómo ejecutar el proyecto localmente
1. Clone este repositorio en tu máquina local.
2. Asegúrese de tener instaladas las dependencias. Puede instalarlas ejecutando:
   ```bash
   pip install customtkinter numpy matplotlib scipy
