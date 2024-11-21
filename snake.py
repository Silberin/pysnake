import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Game speed
speed = 15

# Window size
frame_size_x = 1080
frame_size_y = 720

# Check for errors
check_errors = pygame.init()
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')

# Initialise game window
pygame.display.set_caption("Snake Game")
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# FPS controller
fps_controller = pygame.time.Clock()
# One snake square size
square_size = 60

# Initialize variables
def init_vars():
    global head_pos, snake_body, food_pos, food_spawn, direction, score
    direction = "RIGHT"
    head_pos = [120, 60]
    snake_body = [[120, 60]]
    food_pos = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                random.randrange(1, (frame_size_y // square_size)) * square_size]
    food_spawn = True
    score = 0

init_vars()

# Display score function
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score: {0}'.format(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x / 10, 15)
    else:
        score_rect.midtop = (frame_size_x / 2, frame_size_y / 1.25)
    game_window.blit(score_surface, score_rect)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                direction = 'UP'
            if event.key == pygame.K_DOWN and direction != 'UP':
                direction = 'DOWN'
            if event.key == pygame.K_LEFT and direction != 'RIGHT':
                direction = 'LEFT'
            if event.key == pygame.K_RIGHT and direction != 'LEFT':
                direction = 'RIGHT'

    # Directions
    if direction == 'UP':
        head_pos[1] -= square_size
    if direction == 'DOWN':
        head_pos[1] += square_size
    if direction == 'LEFT':
        head_pos[0] -= square_size
    if direction == 'RIGHT':
        head_pos[0] += square_size

    if head_pos[0] < 0:
        head_pos[0] = frame_size_x - square_size
    elif head_pos[0] > frame_size_x - square_size:
        head_pos[0] = 0
    elif head_pos[1] < 0:
        head_pos[1] = frame_size_y - square_size
    elif head_pos[1] > frame_size_y - square_size:
        head_pos[1] = 0

    # Snake body mechanism
    snake_body.insert(0, list(head_pos))
    if head_pos == food_pos:
        score += 1
        food_spawn = False
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(1, (frame_size_x // square_size)) * square_size,
                    random.randrange(1, (frame_size_y // square_size)) * square_size]
    food_spawn = True

    # Background
    game_window.fill(black)

    # Draw snake
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], square_size, square_size))

    # Draw food
    pygame.draw.rect(game_window, red, pygame.Rect(food_pos[0], food_pos[1], square_size, square_size))

    # Game Over conditions
    for block in snake_body[1:]:
        if head_pos[0] == block[0] and head_pos[1] == block[1]:
            init_vars()

    show_score(1, white, 'times new roman', 20)
    pygame.display.update()
    fps_controller.tick(speed)