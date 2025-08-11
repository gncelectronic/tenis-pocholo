# Tenis Pocholo 3D

Versión básica en 3D del juego de tenis utilizando `pygame` y `PyOpenGL`. La
cancha se representa con perspectiva, los jugadores son figuras simples con
extremidades y raqueta y la pelota una esfera con mayor definición. El jugador
se desplaza lateralmente con las flechas izquierda/derecha y se acerca o aleja
de la red con arriba/abajo. La IA mueve la raqueta contraria. El marcador
aparece en el título de la ventana.

## Requisitos
- Python 3
- pygame
- PyOpenGL

## Ejecución
Instala las dependencias y ejecuta:


```
  pip install pygame PyOpenGL
  python main.py
```

La ventana abre en 1280×720. Mueve al jugador con las flechas izquierda/derecha
para desplazarte por la cancha y con arriba/abajo para acercarte o alejarte de
la red. La pelota rebota en las paredes y cambia de lado al golpear las
raquetas.
