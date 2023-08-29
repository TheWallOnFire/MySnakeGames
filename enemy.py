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
snake_speed = 20
snake_block_size = 10

class MovingBlock:
    def __init__(self, x, y, size, color, direction, border_only=False):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.direction = direction
        self.border_only = border_only
moving_blocks = []

# Initialize pygame
pygame.init()
pygame.display.set_caption('HMT Snakes')
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
            
block_spawn_counter = 0
block_spawn_rate = 10
block_spawn_speed = 10

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

    for block in moving_blocks:
        if block.direction == 'UP':
            block.y -= block_spawn_speed
        elif block.direction == 'DOWN':
            block.y += block_spawn_speed
        elif block.direction == 'LEFT':
            block.x -= block_spawn_speed
        elif block.direction == 'RIGHT':
            block.x += block_spawn_speed

    snake_body.insert(0, list(snake_position))
    if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
        score += 10
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

    for block in moving_blocks:
        pygame.draw.rect(game_window, block.color, pygame.Rect(block.x, block.y, block.size, block.size))

    # Inside the main game loop
    for block in moving_blocks:
        if block.x < 0 or block.x >= window_x or block.y < 0 or block.y >= window_y:
            moving_blocks.remove(block)
        if snake_position[0] == block.x and snake_position[1] == block.y:
            game_over()
        for segment in snake_body:
            if segment[0] == block.x and segment[1] == block.y:
                game_over()
    block_spawn_counter += 1
    if block_spawn_counter >= block_spawn_rate:
        # Generate random position and direction for the new block
        if random.random() < 0.5:
            if random.random() < 0.5:
                block_x = random.choice([0, window_x - snake_block_size])
                block_y = random.randrange(0, window_y // snake_block_size) * snake_block_size
                block_direction = 'RIGHT' if block_x == 0 else 'LEFT'
            else:
                block_x = random.randrange(0, window_x // snake_block_size) * snake_block_size
                block_y = random.choice([0, window_y - snake_block_size])
                block_direction = 'DOWN' if block_y == 0 else 'UP'

            # Create a new MovingBlock instance and add it to the list
            moving_blocks.append(MovingBlock(block_x, block_y, snake_block_size, red, block_direction, True))
        
        block_spawn_counter = 0
    
    # Inside the main game loop, after removing the off-screen blocks
    for block in moving_blocks:
        pygame.draw.rect(game_window, block.color, pygame.Rect(block.x, block.y, block.size, block.size))

    # Inside the main game loop, after the collision detection
    for block in moving_blocks:
        pygame.draw.rect(game_window, block.color, pygame.Rect(block.x, block.y, block.size, block.size))

    if snake_position[0] < 0 or snake_position[0] > window_x - snake_block_size or snake_position[1] < 0 or snake_position[1] > window_y - snake_block_size:
        game_over()

    for block in moving_blocks:
        if snake_position[0] == block.x and snake_position[1] == block.y:
            game_over()

    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    show_score(white)
    pygame.display.update()
    fps.tick(snake_speed)