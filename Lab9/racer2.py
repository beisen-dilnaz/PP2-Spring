import pygame, sys
from pygame.locals import *
import random, time

pygame.init()  # Start pygame

FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Screen settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS = 0
COIN_WEIGHTS = [1, 2, 3]  # Possible coin values
COINS_THRESHOLD = 5  # Number of coins to increase speed

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Load background
background = pygame.image.load('/Users/dilnazbeisenova/Desktop/PP2/Lab8/pics/street.png')

# Set display
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

# Enemy settings
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('/Users/dilnazbeisenova/Desktop/PP2/Lab8/pics/Enemy.png')
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Player settings
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('/Users/dilnazbeisenova/Desktop/PP2/Lab8/pics/Player.png')
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

# Coin settings
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.weight = random.choice(COIN_WEIGHTS)
        self.image = pygame.image.load('/Users/dilnazbeisenova/Desktop/PP2/Lab8/pics/coin.png')
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), random.randint(40, SCREEN_HEIGHT - 100))

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            self.weight = random.choice(COIN_WEIGHTS)

# Create game objects
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Groups

# Enemy group
enemies = pygame.sprite.Group()
enemies.add(E1)

# Coin group
coins = pygame.sprite.Group()
coins.add(C1)

# All sprites group
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Events
INC_SPEED = pygame.USEREVENT + 1  # Speed increase event
pygame.time.set_timer(INC_SPEED, 1000)

SPAWN_COIN = pygame.USEREVENT + 2  # Coin spawning event
pygame.time.set_timer(SPAWN_COIN, 3000)

# Spawn coin function
def spawn_coin():
    new_coin = Coin()
    coins.add(new_coin)
    all_sprites.add(new_coin)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.5

        if event.type == SPAWN_COIN:
            spawn_coin()

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Display background and scores
    DISPLAYSURF.blit(background, (0, 0))
    score_text = font_small.render("Score: " + str(SCORE), True, BLACK)
    coin_text = font_small.render("Coins: " + str(COINS), True, BLACK)
    DISPLAYSURF.blit(score_text, (10, 10))
    DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - 100, 10))

    # Move and draw objects
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        if hasattr(entity, 'move'):
            entity.move()

    # Check collisions with enemies
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('/Users/dilnazbeisenova/Desktop/PP2/Lab8/crash.wav').play()
        time.sleep(0.5)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Check coin collection
    collided_coins = pygame.sprite.spritecollide(P1, coins, True)
    for coin in collided_coins:
        COINS += coin.weight

        # Increase enemy speed after certain coins collected
        if COINS % COINS_THRESHOLD == 0:
            SPEED += 1

    pygame.display.update()
    FramePerSec.tick(FPS)
