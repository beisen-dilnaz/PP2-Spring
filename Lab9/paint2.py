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

                # Task 1: Draw square
                elif tool == "square":
                    size = max(abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                    rect = pygame.Rect(start_pos[0], start_pos[1], size, size)
                    pygame.draw.rect(screen, color, rect, 2)

                # Task 2: Draw right triangle
                elif tool == "right_triangle":
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    points = [(x1, y1), (x1, y2), (x2, y2)]
                    pygame.draw.polygon(screen, color, points, 2)

                # Task 3: Draw equilateral triangle
                elif tool == "equilateral_triangle":
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    side = abs(x2 - x1)
                    height = int((3 ** 0.5 / 2) * side)
                    points = [(x1, y1), (x1 + side, y1), (x1 + side // 2, y1 - height)]
                    pygame.draw.polygon(screen, color, points, 2)

                # Task 4: Draw rhombus
                elif tool == "rhombus":
                    x1, y1 = start_pos
                    x2, y2 = end_pos
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    dx = abs(x2 - x1) // 2
                    dy = abs(y2 - y1) // 2
                    points = [(center_x, y1), (x2, center_y), (center_x, y2), (x1, center_y)]
                    pygame.draw.polygon(screen, color, points, 2)

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

            # Task tool selection (keys: 6 to 0)
            elif event.key == pygame.K_6:
                tool = "square"  # Task 1
            elif event.key == pygame.K_7:
                tool = "right_triangle"  # Task 2
            elif event.key == pygame.K_8:
                tool = "equilateral_triangle"  # Task 3
            elif event.key == pygame.K_9:
                tool = "rhombus"  # Task 4

            elif event.key in COLOR_PALETTE:
                color = COLOR_PALETTE[event.key]

    pygame.display.update()
    clock.tick(60)
