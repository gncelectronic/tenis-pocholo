import pygame
import sys
import random

# Inicializa Pygame y sonidos
pygame.init()
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tenis Pocholo: ¡Cuidado con los salchichas!")
clock = pygame.time.Clock()

# Sonidos (puedes cambiar por tus archivos en assets/)
try:
    pygame.mixer.init()
    sound_score = pygame.mixer.Sound("assets/score.wav")
    sound_dog = pygame.mixer.Sound("assets/dog.wav")
    sound_recover = pygame.mixer.Sound("assets/recover.wav")
except:
    sound_score = sound_dog = sound_recover = None

# Colores
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# Jugador
player_img = pygame.Surface((60, 120), pygame.SRCALPHA)
pygame.draw.ellipse(player_img, WHITE, [0, 0, 60, 120])

# Pelota
ball = pygame.Rect(WIDTH//2-10, HEIGHT//2-10, 20, 20)
ball_speed = [7, 7]

# Perro salchicha
dog_img = pygame.Surface((90, 40), pygame.SRCALPHA)
pygame.draw.ellipse(dog_img, BROWN, [0, 0, 90, 40])
pygame.draw.circle(dog_img, BROWN, (80, 20), 20) # Cabeza

dogs = []
DOG_SPAWN_TIME = 120
dog_timer = 0

# Jugador
player = pygame.Rect(50, HEIGHT//2-60, 60, 120)
player_speed = 10

# Estado de la pelota
ball_taken = False
dog_with_ball = None

# Puntos
score = 0
font = pygame.font.SysFont("Arial", 40)

# Menú de inicio
game_state = "menu"

def spawn_dog():
    y = random.randint(60, HEIGHT-100)
    direction = random.choice([-1, 1])
    if direction == -1:
        x = WIDTH
    else:
        x = -90
    dogs.append({'rect': pygame.Rect(x, y, 90, 40), 'dir': direction, 'has_ball': False})

def reset_ball():
    global ball, ball_speed, ball_taken, dog_with_ball
    ball.x, ball.y = WIDTH//2-10, HEIGHT//2-10
    ball_speed = [random.choice([-7, 7]), random.choice([-7, 7])]
    ball_taken = False
    dog_with_ball = None

def draw():
    screen.fill(GREEN)
    pygame.draw.rect(screen, WHITE, [WIDTH//2-5, 0, 10, HEIGHT])
    screen.blit(player_img, player)
    for dog in dogs:
        screen.blit(dog_img, dog['rect'])
    if not ball_taken:
        pygame.draw.ellipse(screen, RED, ball)
    score_text = font.render(f"Puntos: {score}", True, YELLOW)
    screen.blit(score_text, (WIDTH - 250, 30))
    pygame.display.flip()

def draw_menu():
    screen.fill(GREEN)
    title = font.render("Tenis Pocholo", True, WHITE)
    subtitle = font.render("¡Cuidado con los salchichas!", True, YELLOW)
    start_text = font.render("Presiona ENTER para jugar", True, BLACK)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 100))
    screen.blit(subtitle, (WIDTH//2 - subtitle.get_width()//2, HEIGHT//2 - 30))
    screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2 + 80))
    pygame.display.flip()

def update_dogs():
    global ball_taken, dog_with_ball
    for dog in dogs:
        dog['rect'].x += dog['dir'] * 5
        if dog['rect'].colliderect(ball) and not ball_taken:
            ball_taken = True
            dog['has_ball'] = True
            dog_with_ball = dog
            if sound_dog: sound_dog.play()
        if dog['rect'].x < -100 or dog['rect'].x > WIDTH+100:
            dogs.remove(dog)

def recover_ball():
    global ball_taken, dog_with_ball
    if dog_with_ball and player.colliderect(dog_with_ball['rect']):
        ball.x, ball.y = player.centerx, player.centery
        ball_taken = False
        dog_with_ball['has_ball'] = False
        dog_with_ball = None
        if sound_recover: sound_recover.play()

def add_score():
    global score
    score += 1
    if sound_score: sound_score.play()

def game_loop():
    global dog_timer, game_state, score
    reset_ball()
    score = 0
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
            if ball.top <= 0 or ball.bottom >= HEIGHT:
                ball_speed[1] *= -1
            if ball.left <= 0 or ball.right >= WIDTH:
                add_score()
                reset_ball()

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

# Main loop
while True:
    if game_state == "menu":
        menu_loop()
    elif game_state == "playing":
        game_loop()