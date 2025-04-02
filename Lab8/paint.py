import pygame
import sys

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Paint")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLOR_PALETTE = {
    pygame.K_1: BLACK,
    pygame.K_2: (255, 0, 0),
    pygame.K_3: (0, 255, 0),
    pygame.K_4: (0, 0, 255),
    pygame.K_5: (255, 255, 0),
}

# Initial settings
clock = pygame.time.Clock()
screen.fill(WHITE)
drawing = False
tool = "line"
color = BLACK
start_pos = (0, 0)

ERASER_SIZE = 20

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Start drawing
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                start_pos = event.pos
                drawing = True
                if tool == "line":
                    pygame.draw.circle(screen, color, event.pos, 2)

        # Eraser and free line
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                if tool == "line":
                    pygame.draw.line(screen, color, start_pos, event.pos, 3)
                    start_pos = event.pos
                elif tool == "eraser":
                    pygame.draw.rect(screen, WHITE,
                                     (event.pos[0] - ERASER_SIZE // 2,
                                      event.pos[1] - ERASER_SIZE // 2,
                                      ERASER_SIZE, ERASER_SIZE))

        # Draw shape 
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and drawing:
                end_pos = event.pos
                if tool == "rect":
                    rect = pygame.Rect(min(start_pos[0], end_pos[0]),
                                       min(start_pos[1], end_pos[1]),
                                       abs(end_pos[0] - start_pos[0]),
                                       abs(end_pos[1] - start_pos[1]))
                    pygame.draw.rect(screen, color, rect, 2)
                elif tool == "circle":
                    radius = int(((end_pos[0] - start_pos[0]) ** 2 +
                                  (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                    pygame.draw.circle(screen, color, start_pos, radius, 2)
            drawing = False

        # Tool selection
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                tool = "rect"
            elif event.key == pygame.K_c:
                tool = "circle"
            elif event.key == pygame.K_e:
                tool = "eraser"
            elif event.key == pygame.K_l:
                tool = "line"
            elif event.key in COLOR_PALETTE:
                color = COLOR_PALETTE[event.key]

    pygame.display.update()
    clock.tick(60)