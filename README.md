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
la red. Con la barra espaciadora golpeas la pelota y sacas. El marcador se
muestra en pantalla y se anuncia cuando saca la CPU. La cancha es de color
naranja ladrillo y en los laterales se ven las tribunas. De vez en cuando
aparecen perros salchicha intentando robar la pelota: ¡ahuyéntalos con un
raquetazo usando la misma tecla de golpe!

Los sonidos de golpe y aplauso se generan automáticamente al iniciar el juego,
por lo que no es necesario descargarlos previamente.
