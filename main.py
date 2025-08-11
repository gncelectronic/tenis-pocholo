import sys
import random
import pygame
from pygame.locals import DOUBLEBUF, OPENGL, K_UP, K_DOWN
from OpenGL.GL import *
from OpenGL.GLU import *

WIDTH, HEIGHT = 1000, 600
PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_DEPTH = 1.0, 2.0, 0.3
COURT_HALF_WIDTH, COURT_HALF_DEPTH = 5.0, 7.0


def init():
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)
    gluPerspective(45, WIDTH / HEIGHT, 0.1, 50.0)
    glTranslatef(0.0, -1.5, -20)
    glEnable(GL_DEPTH_TEST)


def draw_court():
    glColor3f(0, 0.5, 0)
    glBegin(GL_QUADS)
    glVertex3f(-COURT_HALF_WIDTH, 0, -COURT_HALF_DEPTH)
    glVertex3f(COURT_HALF_WIDTH, 0, -COURT_HALF_DEPTH)
    glVertex3f(COURT_HALF_WIDTH, 0, COURT_HALF_DEPTH)
    glVertex3f(-COURT_HALF_WIDTH, 0, COURT_HALF_DEPTH)
    glEnd()
    glColor3f(1, 1, 1)
    glBegin(GL_LINES)
    glVertex3f(-COURT_HALF_WIDTH, 0, 0)
    glVertex3f(COURT_HALF_WIDTH, 0, 0)
    glEnd()


def draw_box(x, y, z, w, h, d, color):
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


def draw_ball(position):
    glColor3f(1, 1, 0)
    glPushMatrix()
    glTranslatef(*position)
    quad = gluNewQuadric()
    gluSphere(quad, 0.3, 16, 16)
    gluDeleteQuadric(quad)
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
        if keys[K_UP] and player_pos[1] < 3.5:
            player_pos[1] += 0.2
        if keys[K_DOWN] and player_pos[1] > 0.5:
            player_pos[1] -= 0.2

        if opponent_pos[1] + 0.1 < ball_pos[1]:
            opponent_pos[1] += 0.1
        elif opponent_pos[1] - 0.1 > ball_pos[1]:
            opponent_pos[1] -= 0.1
        opponent_pos[1] = max(0.5, min(3.5, opponent_pos[1]))

        for i in range(3):
            ball_pos[i] += ball_speed[i]
        if ball_pos[1] >= 3.5 or ball_pos[1] <= 0.5:
            ball_speed[1] *= -1

        if ball_pos[2] <= player_pos[2] + PADDLE_DEPTH and ball_pos[2] >= player_pos[2] and abs(ball_pos[0] - player_pos[0]) <= PADDLE_WIDTH and abs(ball_pos[1] - player_pos[1]) <= PADDLE_HEIGHT / 2:
            ball_speed[2] *= -1
        if ball_pos[2] >= opponent_pos[2] - PADDLE_DEPTH and ball_pos[2] <= opponent_pos[2] and abs(ball_pos[0] - opponent_pos[0]) <= PADDLE_WIDTH and abs(ball_pos[1] - opponent_pos[1]) <= PADDLE_HEIGHT / 2:
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
        draw_box(*player_pos, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_DEPTH, (0, 0, 1))
        draw_box(*opponent_pos, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_DEPTH, (1, 0, 0))
        draw_ball(ball_pos)
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
