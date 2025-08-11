import sys
import random

import pygame
from pygame.locals import DOUBLEBUF, OPENGL, K_DOWN, K_UP, K_LEFT, K_RIGHT
from OpenGL.GL import *
from OpenGL.GLU import *

# Window resolution boosted for a clearer view of the court
WIDTH, HEIGHT = 1280, 720

# Dimensions of paddles and play field
PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_DEPTH = 1.0, 2.0, 0.3
COURT_HALF_WIDTH, COURT_HALF_DEPTH = 5.0, 7.0


def init() -> None:
    """Set up pygame and a simple 3D camera."""
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)

    # Basic perspective projection and camera position looking at the court
    gluPerspective(60, WIDTH / HEIGHT, 0.1, 100.0)
    glTranslatef(0.0, -2.0, -25)
    glRotatef(20, 1, 0, 0)

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)


def draw_court() -> None:
    """Render the floor, boundaries and a small net."""
    # Floor
    glColor3f(0, 0.5, 0)
    glBegin(GL_QUADS)
    glVertex3f(-COURT_HALF_WIDTH, 0, -COURT_HALF_DEPTH)
    glVertex3f(COURT_HALF_WIDTH, 0, -COURT_HALF_DEPTH)
    glVertex3f(COURT_HALF_WIDTH, 0, COURT_HALF_DEPTH)
    glVertex3f(-COURT_HALF_WIDTH, 0, COURT_HALF_DEPTH)
    glEnd()

    # Boundary lines
    glColor3f(1, 1, 1)
    glBegin(GL_LINE_LOOP)
    glVertex3f(-COURT_HALF_WIDTH, 0.01, -COURT_HALF_DEPTH)
    glVertex3f(COURT_HALF_WIDTH, 0.01, -COURT_HALF_DEPTH)
    glVertex3f(COURT_HALF_WIDTH, 0.01, COURT_HALF_DEPTH)
    glVertex3f(-COURT_HALF_WIDTH, 0.01, COURT_HALF_DEPTH)
    glEnd()

    # Net
    glBegin(GL_QUADS)
    glVertex3f(-0.05, 0, 0)
    glVertex3f(0.05, 0, 0)
    glVertex3f(0.05, 1.5, 0)
    glVertex3f(-0.05, 1.5, 0)
    glEnd()


def draw_box(x: float, y: float, z: float, w: float, h: float, d: float, color: tuple[float, float, float]) -> None:
    """Render a colored cuboid centered at (x, y, z)."""
    hw, hh, hd = w / 2, h / 2, d / 2
    vertices = [
        (x - hw, y - hh, z - hd),
        (x + hw, y - hh, z - hd),
        (x + hw, y + hh, z - hd),
        (x - hw, y + hh, z - hd),
        (x - hw, y - hh, z + hd),
        (x + hw, y - hh, z + hd),
        (x + hw, y + hh, z + hd),
        (x - hw, y + hh, z + hd),
    ]
    faces = (
        (0, 1, 2, 3),
        (3, 2, 6, 7),
        (1, 5, 6, 2),
        (4, 5, 1, 0),
        (4, 0, 3, 7),
        (5, 4, 7, 6),
    )
    glColor3fv(color)
    glBegin(GL_QUADS)
    for face in faces:
        for v in face:
            glVertex3fv(vertices[v])
    glEnd()


def draw_ball(position: list[float]) -> None:
    """Draw the tennis ball with a smoother sphere."""
    glColor3f(1, 1, 0)
    glPushMatrix()
    glTranslatef(*position)
    quad = gluNewQuadric()
    gluSphere(quad, 0.3, 32, 32)
    gluDeleteQuadric(quad)
    glPopMatrix()


def draw_player(position: list[float], color: tuple[float, float, float]) -> None:
    """Render a simple humanoid figure with limbs and a racket."""
    glPushMatrix()
    glTranslatef(position[0], 0, position[2])

    # Torso
    draw_box(0, 1.0, 0, 0.6, 1.5, 0.3, color)

    # Head
    glColor3f(1, 0.8, 0.6)
    glPushMatrix()
    glTranslatef(0, 1.5 + 0.4, 0)
    quad = gluNewQuadric()
    gluSphere(quad, 0.4, 16, 16)
    gluDeleteQuadric(quad)
    glPopMatrix()

    # Hair
    glColor3f(0.2, 0.1, 0.0)
    glPushMatrix()
    glTranslatef(0, 1.5 + 0.6, 0)
    quad = gluNewQuadric()
    gluSphere(quad, 0.45, 16, 16)
    gluDeleteQuadric(quad)
    glPopMatrix()

    # Arms
    glColor3f(1, 0.8, 0.6)
    for x in (-0.45, 0.45):
        glPushMatrix()
        glTranslatef(x, 1.3, 0)
        glRotatef(90, 0, 0, 1)
        quad = gluNewQuadric()
        gluCylinder(quad, 0.1, 0.1, 0.8, 8, 8)
        gluDeleteQuadric(quad)
        glPopMatrix()

    # Legs
    for x in (-0.2, 0.2):
        glPushMatrix()
        glTranslatef(x, 0.0, 0)
        glRotatef(90, 1, 0, 0)
        quad = gluNewQuadric()
        gluCylinder(quad, 0.15, 0.15, 1.0, 8, 8)
        gluDeleteQuadric(quad)
        glPopMatrix()

    # Racket in right hand
    glColor3f(0.8, 0.8, 0.8)
    glPushMatrix()
    glTranslatef(0.9, 1.3, 0)
    glRotatef(90, 0, 0, 1)
    quad = gluNewQuadric()
    gluCylinder(quad, 0.05, 0.05, 0.5, 8, 8)
    glTranslatef(0, 0, 0.5)
    gluCylinder(quad, 0.2, 0.2, 0.1, 16, 16)
    gluDeleteQuadric(quad)
    glPopMatrix()

    glPopMatrix()


def reset_ball(ball_pos, ball_speed):
    ball_pos[:] = [0.0, 1.5, 0.0]
    direction = random.choice([-1, 1])
    ball_speed[:] = [0.1 * direction, 0.05, 0.2 * direction]


def main():
    init()
    clock = pygame.time.Clock()
    player_pos = [0.0, 1.5, -COURT_HALF_DEPTH + 0.5]
    opponent_pos = [0.0, 1.5, COURT_HALF_DEPTH - 0.5]
    ball_pos = [0.0, 1.5, 0.0]
    ball_speed = [0.1, 0.05, 0.2]
    player_score = opponent_score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and player_pos[0] > -COURT_HALF_WIDTH + PADDLE_WIDTH / 2:
            player_pos[0] -= 0.2
        if keys[K_RIGHT] and player_pos[0] < COURT_HALF_WIDTH - PADDLE_WIDTH / 2:
            player_pos[0] += 0.2
        if keys[K_UP] and player_pos[2] < -PADDLE_DEPTH:
            player_pos[2] += 0.2
        if keys[K_DOWN] and player_pos[2] > -COURT_HALF_DEPTH + PADDLE_DEPTH:
            player_pos[2] -= 0.2

        if opponent_pos[0] + 0.1 < ball_pos[0]:
            opponent_pos[0] += 0.1
        elif opponent_pos[0] - 0.1 > ball_pos[0]:
            opponent_pos[0] -= 0.1
        opponent_pos[0] = max(-COURT_HALF_WIDTH + PADDLE_WIDTH / 2, min(COURT_HALF_WIDTH - PADDLE_WIDTH / 2, opponent_pos[0]))

        for i in range(3):
            ball_pos[i] += ball_speed[i]
        if ball_pos[1] >= 3.5 or ball_pos[1] <= 0.5:
            ball_speed[1] *= -1

        if (
            ball_pos[2] <= player_pos[2] + PADDLE_DEPTH
            and ball_pos[2] >= player_pos[2]
            and abs(ball_pos[0] - player_pos[0]) <= PADDLE_WIDTH
            and abs(ball_pos[1] - 1.5) <= PADDLE_HEIGHT / 2
        ):
            ball_speed[2] *= -1
        if (
            ball_pos[2] >= opponent_pos[2] - PADDLE_DEPTH
            and ball_pos[2] <= opponent_pos[2]
            and abs(ball_pos[0] - opponent_pos[0]) <= PADDLE_WIDTH
            and abs(ball_pos[1] - 1.5) <= PADDLE_HEIGHT / 2
        ):
            ball_speed[2] *= -1

        if ball_pos[2] < -COURT_HALF_DEPTH:
            opponent_score += 1
            reset_ball(ball_pos, ball_speed)
        elif ball_pos[2] > COURT_HALF_DEPTH:
            player_score += 1
            reset_ball(ball_pos, ball_speed)

        pygame.display.set_caption(f"Tenis Pocholo 3D - {player_score} : {opponent_score}")

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_court()
        draw_player(player_pos, (0, 0, 1))
        draw_player(opponent_pos, (1, 0, 0))
        draw_ball(ball_pos)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
