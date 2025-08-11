# Tenis Pocholo 3D

Versión básica en 3D del juego de tenis utilizando `pygame` y `PyOpenGL`. La
cancha se representa con perspectiva, los jugadores son bloques y la pelota una
esfera. El jugador controla la raqueta frontal con las flechas arriba/abajo y la
IA mueve la raqueta contraria. El marcador aparece en el título de la ventana.

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

Mueve al jugador con las flechas arriba/abajo. La pelota rebota en las paredes
y cambia de lado al golpear las raquetas.
