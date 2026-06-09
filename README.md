# Visualizador de Búsqueda IA

Este proyecto es una aplicación interactiva desarrollada con **Streamlit** que permite visualizar el funcionamiento de distintos algoritmos de Inteligencia Artificial (Búsqueda Adversaria, Búsqueda Local, Búsqueda No Informada y Búsqueda Informada) aplicados a juegos y rompecabezas clásicos.

## Problemas Implementados

- **Gato (Tic-Tac-Toe)**: Búsqueda Adversaria (algoritmo Minimax).
- **8 Reinas**: Búsqueda Local (algoritmos Hill Climbing y Simulated Annealing).
- **Frozen Lake**: Búsqueda No Informada (algoritmos BFS y DFS).
- **Sokoban**: Búsqueda Informada (A* y Greedy) _[Por implementar/En desarrollo]_.

## Requisitos y Dependencias

Asegúrate de tener instalado Python (Mínimo `3.9+` recomendado).

Para ejecutar el proyecto necesitas instalar las dependencias principales. Puedes hacerlo fácilmente usando `pip`:

```bash
pip install streamlit
pip install streamlit-option-menu
pip install numpy
```

### Explicación de librerías
- `streamlit`: Framework principal utilizado para crear toda la interfaz web de manera rápida y con componentes minimalistas.
- `streamlit-option-menu`: Componente externo usado en la barra de navegación lateral para darle un diseño moderno e incluir iconos.
- `numpy`: Librería base de Python empleada para el manejo fácil de arreglos numéricos y manipulación vectorial de datos (muy útil para inicializar estados aleatorios como en el juego de las 8 Reinas).

## Instrucciones de Ejecución

1. Clona este repositorio o descarga la carpeta en tu entorno local.
2. Abre una terminal dentro de la raíz del proyecto (donde se encuentra el archivo `app.py`).
3. Instala las librerías mencionadas anteriormente si no las tienes.
4. Ejecuta el siguiente comando para levantar el servidor web:

```bash
streamlit run app.py
```

5. El navegador se abrirá automáticamente en `http://localhost:8501/` con la aplicación en un entorno interactivo y minimalista.