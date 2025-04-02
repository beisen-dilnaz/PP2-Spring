import pygame

pygame.init()
WIDTH, HEIGHT = 500, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

ball_x, ball_y = WIDTH // 2, HEIGHT // 2
BALL_RADIUS = 25
SPEED = 20

running = True
while running:
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (5, 255, 0), (ball_x, ball_y), BALL_RADIUS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and ball_x - BALL_RADIUS > 0:
        ball_x -= SPEED
    if keys[pygame.K_RIGHT] and ball_x + BALL_RADIUS < WIDTH:
        ball_x += SPEED
    if keys[pygame.K_UP] and ball_y - BALL_RADIUS > 0:
        ball_y -= SPEED
    if keys[pygame.K_DOWN] and ball_y + BALL_RADIUS < HEIGHT:
        ball_y += SPEED

    pygame.display.flip()
    clock.tick(30)

pygame.quit()