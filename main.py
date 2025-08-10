import pygame
import sys
import random

pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tenis Pocholo: ¡Cuidado con los salchichas!")
clock = pygame.time.Clock()

try:
    pygame.mixer.init()
    sound_score = pygame.mixer.Sound("assets/score.wav")
    sound_dog = pygame.mixer.Sound("assets/dog.wav")
    sound_recover = pygame.mixer.Sound("assets/recover.wav")
except Exception:
    sound_score = sound_dog = sound_recover = None

# Colores
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
SKIN = (255, 224, 189)
BLUE = (30, 144, 255)
FLUO_YELLOW = (204, 255, 0)

# Jugadores
def create_player_image(color):
    img = pygame.Surface((80, 120), pygame.SRCALPHA)
    # Piernas
    pygame.draw.rect(img, BLACK, (15, 80, 12, 40))
    pygame.draw.rect(img, BLACK, (33, 80, 12, 40))
    # Torso
    pygame.draw.rect(img, color, (15, 40, 30, 40))
    # Brazo sosteniendo la raqueta
    pygame.draw.rect(img, SKIN, (45, 45, 20, 10))
    # Raqueta (mango y aro)
    pygame.draw.rect(img, BLACK, (60, 40, 5, 25))
    pygame.draw.ellipse(img, WHITE, (55, 20, 25, 25))
    pygame.draw.ellipse(img, BLACK, (55, 20, 25, 25), 2)
    # Cabeza
    pygame.draw.circle(img, SKIN, (30, 20), 20)
    # Detalles del rostro estilo Double Dragon
    pygame.draw.rect(img, color, (10, 10, 40, 5))  # cinta en la cabeza
    pygame.draw.circle(img, BLACK, (22, 18), 3)  # ojo izquierdo
    pygame.draw.circle(img, BLACK, (38, 18), 3)  # ojo derecho
    pygame.draw.line(img, BLACK, (22, 30), (38, 30), 3)  # boca
    return img

player_img = create_player_image(BLUE)
player = pygame.Rect(60, HEIGHT // 2 - 60, 80, 120)
player_speed = 10

opponent_img = create_player_image(RED)
opponent = pygame.Rect(WIDTH - 140, HEIGHT // 2 - 60, 80, 120)
opponent_speed = 7

# Pelota
ball = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)
ball_speed = [7, 7]

# Perros salchicha
def create_dog_image():
    img = pygame.Surface((120, 60), pygame.SRCALPHA)
    # Cuerpo alargado típico del salchicha
    pygame.draw.ellipse(img, BROWN, [10, 25, 90, 25])
    # Cabeza con hocico
    pygame.draw.circle(img, BROWN, (100, 37), 15)
    pygame.draw.circle(img, BLACK, (110, 37), 3)  # nariz
    # Oreja caída
    pygame.draw.ellipse(img, BROWN, [95, 25, 18, 20])
    # Cola
    pygame.draw.polygon(img, BROWN, [(10, 35), (0, 30), (0, 40)])
    # Patas cortas
    for x in (25, 45, 65, 85):
        pygame.draw.rect(img, BROWN, (x, 43, 10, 15))
        pygame.draw.rect(img, BLACK, (x, 43, 10, 15), 1)
    return img

dog_img = create_dog_image()
dogs = []
DOG_SPAWN_TIME = 180
dog_timer = 0

# Estado de la pelota
ball_taken = False
dog_with_ball = None

# Puntos
player_score = 0
opponent_score = 0
font = pygame.font.SysFont("Arial", 40)

# Menú
game_state = "menu"

def spawn_dog():
    y = random.randint(60, HEIGHT - 110)
    direction = random.choice([-1, 1])
    x = WIDTH if direction == -1 else -120
    dogs.append({"rect": pygame.Rect(x, y, 120, 60), "dir": direction, "has_ball": False})

def reset_ball(direction=None):
    global ball, ball_speed, ball_taken, dog_with_ball
    ball.x, ball.y = WIDTH // 2 - 10, HEIGHT // 2 - 10
    ball_speed = [random.choice([-7, 7]) if direction is None else direction, random.choice([-7, 7])]
    ball_taken = False
    dog_with_ball = None

def draw_court():
    screen.fill(GREEN)
    pygame.draw.rect(screen, WHITE, (50, 50, WIDTH - 100, HEIGHT - 100), 5)
    pygame.draw.line(screen, WHITE, (WIDTH // 2, 50), (WIDTH // 2, HEIGHT - 50), 5)

def draw():
    draw_court()
    screen.blit(player_img, player)
    screen.blit(opponent_img, opponent)
    for dog in dogs:
        screen.blit(dog_img, dog["rect"])
    pygame.draw.ellipse(screen, FLUO_YELLOW, ball)
    score_text = font.render(f"Jugador: {player_score}  CPU: {opponent_score}", True, YELLOW)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
    pygame.display.flip()

def draw_menu():
    screen.fill(GREEN)
    title = font.render("Tenis Pocholo", True, WHITE)
    subtitle = font.render("¡Cuidado con los salchichas!", True, YELLOW)
    start_text = font.render("Presiona ENTER para jugar", True, BROWN)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(subtitle, (WIDTH // 2 - subtitle.get_width() // 2, HEIGHT // 2 - 30))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 80))
    pygame.display.flip()

def update_dogs():
    global ball_taken, dog_with_ball
    for dog in dogs[:]:
        dog["rect"].x += dog["dir"] * 5
        if dog["rect"].colliderect(ball) and not ball_taken:
            ball_taken = True
            dog["has_ball"] = True
            dog_with_ball = dog
            if sound_dog:
                sound_dog.play()
        if dog["has_ball"]:
            ball.center = dog["rect"].center
        if dog["rect"].x < -150 or dog["rect"].x > WIDTH + 150:
            dogs.remove(dog)
            if dog is dog_with_ball:
                reset_ball(direction=random.choice([-7, 7]))

def recover_ball():
    global ball_taken, dog_with_ball
    if dog_with_ball and player.colliderect(dog_with_ball["rect"]):
        ball.center = player.center
        ball_taken = False
        dog_with_ball["has_ball"] = False
        dog_with_ball = None
        if sound_recover:
            sound_recover.play()

def update_opponent():
    if opponent.centery < ball.centery:
        opponent.y += opponent_speed
    elif opponent.centery > ball.centery:
        opponent.y -= opponent_speed
    opponent.y = max(0, min(opponent.y, HEIGHT - opponent.height))

def add_score(left_side):
    global player_score, opponent_score
    if left_side:
        opponent_score += 1
    else:
        player_score += 1
    if sound_score:
        sound_score.play()

def game_loop():
    global dog_timer, game_state
    reset_ball()
    while game_state == "playing":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player.top > 0:
            player.y -= player_speed
        if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
            player.y += player_speed
        if keys[pygame.K_SPACE] and ball_taken:
            recover_ball()

        if not ball_taken:
            ball.x += ball_speed[0]
            ball.y += ball_speed[1]
            if ball.top <= 50 or ball.bottom >= HEIGHT - 50:
                ball_speed[1] *= -1
            if ball.colliderect(player):
                ball_speed[0] = abs(ball_speed[0])
            if ball.colliderect(opponent):
                ball_speed[0] = -abs(ball_speed[0])
            if ball.left <= 50:
                add_score(left_side=True)
                reset_ball(direction=7)
            if ball.right >= WIDTH - 50:
                add_score(left_side=False)
                reset_ball(direction=-7)

        update_opponent()

        dog_timer += 1
        if dog_timer >= DOG_SPAWN_TIME:
            spawn_dog()
            dog_timer = 0

        update_dogs()
        draw()
        clock.tick(60)

def menu_loop():
    global game_state
    while game_state == "menu":
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                game_state = "playing"

while True:
    if game_state == "menu":
        menu_loop()
    elif game_state == "playing":
        game_loop()
