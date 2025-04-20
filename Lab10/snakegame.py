""" first i wrote in terminal:
psql -U phonebook_user -d phonebook_db, then

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS user_scores (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    score INTEGER,
    level INTEGER,
    saved_at TIMESTAMP DEFAULT NOW()
);   """

import pygame
import random
import psycopg2
from datetime import datetime

# Setup
conn = psycopg2.connect(
    dbname="phonebook_db",
    user="phonebook_user",
    password="password",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Init
pygame.init()
WIDTH, HEIGHT = 600, 600
CELL_SIZE = 20
COLS, ROWS = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

# Functions
def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, (0, 255, 0), (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_food(food):
    pygame.draw.rect(screen, (255, 0, 0), (food[0]*CELL_SIZE, food[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_ui(score, level):
    screen.blit(font.render(f"Score: {score}", True, (255,255,255)), (10,10))
    lvl_text = font.render(f"Level: {level}", True, (255,255,255))
    screen.blit(lvl_text, (WIDTH - lvl_text.get_width() - 10, 10))

# Db functions
def get_user(username):
    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    if not user:
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
        conn.commit()
        return cur.fetchone()[0]
    return user[0]

def get_last_state(user_id):
    cur.execute("SELECT score, level FROM user_scores WHERE user_id = %s ORDER BY saved_at DESC LIMIT 1", (user_id,))
    return cur.fetchone()

def save_state(user_id, score, level):
    cur.execute("INSERT INTO user_scores (user_id, score, level) VALUES (%s, %s, %s)", (user_id, score, level))
    conn.commit()

# Food
def generate_food(snake, walls):
    while True:
        pos = [random.randint(0, COLS - 1), random.randint(0, ROWS - 1)]
        if pos not in snake and pos not in walls:
            return pos

# Game setup
username = input("Enter your username: ")
user_id = get_user(username)
last = get_last_state(user_id)

snake = [[5, 5]]
direction = [1, 0]
walls = []
food = generate_food(snake, walls)
score = last[0] if last else 0
level = last[1] if last else 1
speed = 5 + (level - 1) * 1.5
food_to_level = 3

running = True
paused = False

# Game loop
while running:
    clock.tick(speed)
    screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and direction != [0, 1]: direction = [0, -1]
    elif keys[pygame.K_DOWN] and direction != [0, -1]: direction = [0, 1]
    elif keys[pygame.K_LEFT] and direction != [1, 0]: direction = [-1, 0]
    elif keys[pygame.K_RIGHT] and direction != [-1, 0]: direction = [1, 0]
    elif keys[pygame.K_p]:  
        save_state(user_id, score, level)
        paused = True
        print("Game Paused & Saved.")
        while paused:
            for e in pygame.event.get():
                if e.type == pygame.KEYDOWN and e.key == pygame.K_p:
                    print("Game Resumed.")
                    paused = False

    # Move snake
    new_head = [snake[0][0] + direction[0], snake[0][1] + direction[1]]

    if (new_head in snake or not 0 <= new_head[0] < COLS or not 0 <= new_head[1] < ROWS):
        print("Game Over!")
        save_state(user_id, score, level)
        break

    snake.insert(0, new_head)
    if new_head == food:
        score += 1
        food = generate_food(snake, walls)
        if score % food_to_level == 0:
            level += 1
            speed += 1.5
    else:
        snake.pop()

    draw_snake(snake)
    draw_food(food)
    draw_ui(score, level)
    pygame.display.flip()

pygame.quit()
cur.close()
conn.close()