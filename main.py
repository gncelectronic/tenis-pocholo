import sys
import random
from pathlib import Path

import pygame
from pygame.locals import DOUBLEBUF, OPENGL, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_SPACE
from OpenGL.GL import *
from OpenGL.GLU import *
from generate_assets import generate_hit, generate_applause

# Window resolution boosted for a clearer view of the court
WIDTH, HEIGHT = 1280, 720

# Dimensions of paddles and play field
PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_DEPTH = 1.0, 2.0, 0.3
COURT_HALF_WIDTH, COURT_HALF_DEPTH = 5.0, 7.0

ASSETS_DIR = Path("assets")
HIT_FILE = ASSETS_DIR / "hit.wav"
APPLAUSE_FILE = ASSETS_DIR / "applause.wav"
if not HIT_FILE.exists():
    generate_hit(str(HIT_FILE))
if not APPLAUSE_FILE.exists():
    generate_applause(str(APPLAUSE_FILE))


def init() -> None:
    """Set up pygame and a simple 3D camera."""
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_mode((WIDTH, HEIGHT), DOUBLEBUF | OPENGL)

    # Basic perspective projection and camera position looking at the court
    gluPerspective(60, WIDTH / HEIGHT, 0.1, 100.0)
    glTranslatef(0.0, -2.0, -25)
    glRotatef(20, 1, 0, 0)

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.0, 0.0, 0.0, 1.0)


def draw_court() -> None:
    """Render the floor, boundaries and a basic 3D net."""
    # Floor
    glColor3f(0.9, 0.4, 0.1)
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

    # Net posts
    glColor3f(1, 1, 1)
    glBegin(GL_QUADS)
    # Left post
    glVertex3f(-COURT_HALF_WIDTH, 0, -0.05)
    glVertex3f(-COURT_HALF_WIDTH, 0, 0.05)
    glVertex3f(-COURT_HALF_WIDTH, 1.5, 0.05)
    glVertex3f(-COURT_HALF_WIDTH, 1.5, -0.05)
    # Right post
    glVertex3f(COURT_HALF_WIDTH, 0, -0.05)
    glVertex3f(COURT_HALF_WIDTH, 0, 0.05)
    glVertex3f(COURT_HALF_WIDTH, 1.5, 0.05)
    glVertex3f(COURT_HALF_WIDTH, 1.5, -0.05)
    glEnd()

    # Net mesh
    glColor3f(1, 1, 1)
    glBegin(GL_LINES)
    x = -COURT_HALF_WIDTH
    while x <= COURT_HALF_WIDTH:
        glVertex3f(x, 0, 0)
        glVertex3f(x, 1.5, 0)
        x += 0.5
    y = 0.0
    while y <= 1.5:
        glVertex3f(-COURT_HALF_WIDTH, y, 0)
        glVertex3f(COURT_HALF_WIDTH, y, 0)
        y += 0.25
    glEnd()

    # Top band
    glBegin(GL_QUADS)
    glVertex3f(-COURT_HALF_WIDTH, 1.4, 0)
    glVertex3f(COURT_HALF_WIDTH, 1.4, 0)
    glVertex3f(COURT_HALF_WIDTH, 1.5, 0)
    glVertex3f(-COURT_HALF_WIDTH, 1.5, 0)
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


def draw_stands() -> None:
    """Draw simple stands with a cheering crowd along the sidelines."""
    # Stands structures
    stand_color = (0.3, 0.3, 0.3)
    draw_box(-COURT_HALF_WIDTH - 1.5, 1.5, 0, 2.0, 3.0, COURT_HALF_DEPTH * 2 + 2, stand_color)
    draw_box(COURT_HALF_WIDTH + 1.5, 1.5, 0, 2.0, 3.0, COURT_HALF_DEPTH * 2 + 2, stand_color)

    # Simple crowd blocks with random colors to simulate cheering
    for side in (-COURT_HALF_WIDTH - 1.5, COURT_HALF_WIDTH + 1.5):
        z = -COURT_HALF_DEPTH
        while z <= COURT_HALF_DEPTH:
            crowd_color = (random.random(), random.random(), random.random())
            draw_box(side, 1.5, z, 1.8, 1.0, 0.8, crowd_color)
            z += 2.0


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


class Dog:
    """Simple dachshund chasing the ball."""

    def __init__(self, x: float, z: float) -> None:
        self.x = x
        self.z = z
        self.speed = 0.05

    def move_towards(self, target: list[float]) -> None:
        dx = target[0] - self.x
        dz = target[2] - self.z
        dist = max((dx * dx + dz * dz) ** 0.5, 0.001)
        self.x += self.speed * dx / dist
        self.z += self.speed * dz / dist

    def draw(self) -> None:
        draw_box(self.x, 0.25, self.z, 1.0, 0.5, 0.3, (0.6, 0.3, 0.1))


def reset_ball(ball_pos, ball_speed, server, player_pos, opponent_pos):
    if server == "player":
        ball_pos[:] = [player_pos[0], 1.5, player_pos[2] - PADDLE_DEPTH]
        ball_speed[:] = [0.0, 0.0, 0.0]
        return True
    else:
        ball_pos[:] = [opponent_pos[0], 1.5, opponent_pos[2] + PADDLE_DEPTH]
        ball_speed[:] = [0.1 * random.choice([-1, 1]), 0.05, 0.2]
        return False


def main():
    init()
    clock = pygame.time.Clock()
    player_pos = [0.0, 1.5, COURT_HALF_DEPTH - 0.5]
    opponent_pos = [0.0, 1.5, -COURT_HALF_DEPTH + 0.5]
    ball_pos = [0.0, 1.5, 0.0]
    ball_speed = [0.0, 0.0, 0.0]
    player_score = opponent_score = 0
    server = "opponent"
    waiting_for_serve = reset_ball(ball_pos, ball_speed, server, player_pos, opponent_pos)
    opponent_serving_timer = 120
    dogs: list[Dog] = []

    font = pygame.font.SysFont(None, 48)
    hit_sound = pygame.mixer.Sound(str(HIT_FILE))
    score_sound = pygame.mixer.Sound(str(APPLAUSE_FILE))

    while True:
        space_pressed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == K_SPACE:
                space_pressed = True

        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and player_pos[0] > -COURT_HALF_WIDTH + PADDLE_WIDTH / 2:
            player_pos[0] -= 0.2
        if keys[K_RIGHT] and player_pos[0] < COURT_HALF_WIDTH - PADDLE_WIDTH / 2:
            player_pos[0] += 0.2
        if keys[K_UP] and player_pos[2] > PADDLE_DEPTH:
            player_pos[2] -= 0.2
        if keys[K_DOWN] and player_pos[2] < COURT_HALF_DEPTH - PADDLE_DEPTH:
            player_pos[2] += 0.2

        if opponent_pos[0] + 0.1 < ball_pos[0]:
            opponent_pos[0] += 0.1
        elif opponent_pos[0] - 0.1 > ball_pos[0]:
            opponent_pos[0] -= 0.1
        opponent_pos[0] = max(
            -COURT_HALF_WIDTH + PADDLE_WIDTH / 2,
            min(COURT_HALF_WIDTH - PADDLE_WIDTH / 2, opponent_pos[0]),
        )

        # Spawn dogs on player's side
        if not waiting_for_serve and ball_pos[2] > 0 and random.random() < 0.01:
            spawn_z = random.uniform(0, COURT_HALF_DEPTH)
            spawn_x = random.choice([-COURT_HALF_WIDTH - 1.5, COURT_HALF_WIDTH + 1.5])
            dogs.append(Dog(spawn_x, spawn_z))

        if not waiting_for_serve:
            for i in range(3):
                ball_pos[i] += ball_speed[i]
        if ball_pos[1] >= 3.5 or ball_pos[1] <= 0.5:
            ball_speed[1] *= -1

        # Dogs chase the ball
        for dog in dogs[:]:
            dog.move_towards(ball_pos)
            if ((dog.x - ball_pos[0]) ** 2 + (dog.z - ball_pos[2]) ** 2) ** 0.5 < 0.5:
                waiting_for_serve = reset_ball(ball_pos, ball_speed, "player", player_pos, opponent_pos)
                dogs.remove(dog)
            elif space_pressed and ((dog.x - player_pos[0]) ** 2 + (dog.z - player_pos[2]) ** 2) ** 0.5 < 1.5:
                dogs.remove(dog)
                hit_sound.play()

        player_hit = (
            ball_pos[2] >= player_pos[2] - PADDLE_DEPTH
            and ball_pos[2] <= player_pos[2]
            and abs(ball_pos[0] - player_pos[0]) <= PADDLE_WIDTH
            and abs(ball_pos[1] - 1.5) <= PADDLE_HEIGHT / 2
        )
        if player_hit and space_pressed:
            ball_speed[2] = -abs(ball_speed[2])
            hit_sound.play()

        opponent_hit = (
            ball_pos[2] <= opponent_pos[2] + PADDLE_DEPTH
            and ball_pos[2] >= opponent_pos[2]
            and abs(ball_pos[0] - opponent_pos[0]) <= PADDLE_WIDTH
            and abs(ball_pos[1] - 1.5) <= PADDLE_HEIGHT / 2
        )
        if opponent_hit:
            ball_speed[2] = abs(ball_speed[2])
            hit_sound.play()

        if ball_pos[2] > COURT_HALF_DEPTH:
            opponent_score += 1
            score_sound.play()
            server = "opponent"
            waiting_for_serve = reset_ball(ball_pos, ball_speed, server, player_pos, opponent_pos)
            opponent_serving_timer = 120
            dogs.clear()
        elif ball_pos[2] < -COURT_HALF_DEPTH:
            player_score += 1
            score_sound.play()
            server = "player"
            waiting_for_serve = reset_ball(ball_pos, ball_speed, server, player_pos, opponent_pos)
            dogs.clear()

        if waiting_for_serve and space_pressed:
            ball_speed[:] = [0.1 * random.choice([-1, 1]), 0.05, -0.2]
            waiting_for_serve = False
            hit_sound.play()

        pygame.display.set_caption(
            f"Tenis Pocholo 3D - {player_score} : {opponent_score}"
        )

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_court()
        draw_stands()
        draw_player(player_pos, (0, 0, 1))
        draw_player(opponent_pos, (1, 0, 0))
        draw_ball(ball_pos)
        for dog in dogs:
            dog.draw()

        glDisable(GL_DEPTH_TEST)
        screen = pygame.display.get_surface()
        score_text = font.render(
            f"Jugador {player_score} - CPU {opponent_score}", True, (255, 255, 255)
        )
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
        if waiting_for_serve:
            msg = font.render("Tu saque - ESPACIO", True, (255, 255, 0))
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 60))
        elif opponent_serving_timer > 0:
            msg = font.render("CPU saca!", True, (255, 255, 0))
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, 60))
            opponent_serving_timer -= 1
        glEnable(GL_DEPTH_TEST)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
