import pygame
import random

pygame.init()

# Screen and grid setup
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 180, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Setup screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# Draw snake
def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Draw walls
def draw_walls(walls):
    for wall in walls:
        pygame.draw.rect(screen, DARK_GREEN, (wall[0] * CELL_SIZE, wall[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

# Generate food with random weight
def generate_food(snake, walls):
    while True:
        pos = [random.randint(0, COLS - 1), random.randint(0, ROWS - 1)]
        if pos not in snake and pos not in walls:
            weight = random.randint(1, 5)  # Random weight between 1 and 5
            timer = pygame.time.get_ticks()  # Start timer
            return {'pos': pos, 'weight': weight, 'timer': timer}

# Draw food with size based on weight
def draw_food(food):
    size = CELL_SIZE + (food['weight'] - 1) * 3  # Bigger food for higher weight
    offset = (CELL_SIZE - size) // 2
    pygame.draw.rect(screen, RED, (food['pos'][0] * CELL_SIZE + offset, food['pos'][1] * CELL_SIZE + offset, size, size))

# Draw score and level
def draw_ui(score, level):
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))

# Initial game setup
snake = [[5, 5]]
direction = [1, 0]
food = generate_food(snake, [])
walls = []
score = 0
level = 1
speed = 5
food_to_level = 3
food_lifetime = 8000  # Food disappears after 8000 ms (8 seconds)

# Main game loop
running = True
while running:
    clock.tick(speed)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Snake controls
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != [0, 1]:
        direction = [0, -1]
    elif keys[pygame.K_DOWN] and direction != [0, -1]:
        direction = [0, 1]
    elif keys[pygame.K_LEFT] and direction != [1, 0]:
        direction = [-1, 0]
    elif keys[pygame.K_RIGHT] and direction != [-1, 0]:
        direction = [1, 0]

    # Move snake
    new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]

    # Check collisions
    if (new_head in snake or new_head in walls or
        not 0 <= new_head[0] < COLS or
        not 0 <= new_head[1] < ROWS):
        running = False

    snake.insert(0, new_head)

    # Check if snake eats food
    current_time = pygame.time.get_ticks()
    if new_head == food['pos']:
        score += food['weight']  # Increase score by food's weight
        food = generate_food(snake, walls)

        # Level up
        if score % food_to_level == 0:
            level += 1
            speed += 1.5
    else:
        snake.pop()

    # Check food lifetime
    if current_time - food['timer'] > food_lifetime:
        food = generate_food(snake, walls)  # Generate new food if timer expires

    # Draw all game elements
    draw_snake(snake)
    draw_food(food)
    draw_walls(walls)
    draw_ui(score, level)

    pygame.display.flip()

pygame.quit()
