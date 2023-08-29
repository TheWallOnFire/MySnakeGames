import pygame
import time
import random

# Window size
window_x = 720
window_y = 480

# Colors
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)

# Snake properties
snake_speed = 10
snake_speed_up = 1
snake_block_size = 10

# Initialize pygame
pygame.init()
pygame.display.set_caption('Snakes game by HMT')
game_window = pygame.display.set_mode((window_x, window_y))
fps = pygame.time.Clock()

# Font settings
score_font = pygame.font.SysFont('times new roman', 20)
game_over_font = pygame.font.SysFont('times new roman', 50)

# Game variables
snake_position = [window_x//2, window_y//2]
snake_body = [[window_x//2, window_y//2], [window_x//2 - snake_block_size,  window_y//2]]
fruit_position = [random.randrange(1, (window_x // snake_block_size)) * snake_block_size, random.randrange(1, (window_y // snake_block_size)) * snake_block_size]
fruit_spawn = True
direction = 'RIGHT'
change_to = direction
score = 0

# Display score
def show_score(color):
    score_surface = score_font.render('Score: ' + str(score), True, color)
    game_window.blit(score_surface, (10, 10))

# Game over
def game_over():
    game_over_surface = game_over_font.render('Your Score is: ' + str(score), True, red)
    game_over_rect = game_over_surface.get_rect(center=(window_x/2, window_y/2))
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()
    time.sleep(2)
    pygame.quit()
    quit()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and direction != 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                change_to = 'RIGHT'

    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    elif change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    elif change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    elif change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'

    if direction == 'UP':
        snake_position[1] -= snake_block_size
    elif direction == 'DOWN':
        snake_position[1] += snake_block_size
    elif direction == 'LEFT':
        snake_position[0] -= snake_block_size
    elif direction == 'RIGHT':
        snake_position[0] += snake_block_size

    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
        snake_speed += snake_speed_up
        fruit_spawn = False
    else:
        snake_body.pop()

    if not fruit_spawn:
        fruit_position = [random.randrange(1, (window_x // snake_block_size)) * snake_block_size, random.randrange(1, (window_y // snake_block_size)) * snake_block_size]

    fruit_spawn = True
    game_window.fill(black)
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], snake_block_size, snake_block_size))
    pygame.draw.rect(game_window, white, pygame.Rect(fruit_position[0], fruit_position[1], snake_block_size, snake_block_size))

    if snake_position[0] < 0 or snake_position[0] > window_x - snake_block_size or snake_position[1] < 0 or snake_position[1] > window_y - snake_block_size:
        game_over()

    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    show_score(white)
    pygame.display.update()
    fps.tick(snake_speed)