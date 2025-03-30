import pygame
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
screen.fill((255, 255, 255))

# Common colors
C_WHITE = (255, 255, 255)
C_BLACK = (0, 0, 0)
C_RED = (255, 0, 0)
C_BLUE = (0, 0, 255)
C_GREEN = (0, 255, 0)

color = C_RED       # Initial drawing color
radius = 5          # Line thickness
clock = pygame.time.Clock()

drawing = False     # Flag to check if drawing is in progress
start_pos = None    # Stores the mouse down position

# Current drawing mode (line/square/triangle/etc.)
current_shape = "line"

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse button pressed: start drawing
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        # Mouse button released: stop drawing and draw the shape
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            x1, y1 = start_pos
            x2, y2 = end_pos

            if current_shape == "line":
                pygame.draw.line(screen, color, start_pos, end_pos, radius)

            elif current_shape == "square":
                side = min(abs(x2 - x1), abs(y2 - y1))
                rect = pygame.Rect(x1, y1, side, side)
                pygame.draw.rect(screen, color, rect, radius)

            elif current_shape == "right_triangle":
                # Right triangle with a horizontal base and vertical height
                points = [start_pos, (x1, y2), (x2, y2)]
                pygame.draw.polygon(screen, color, points, radius)

            elif current_shape == "equilateral_triangle":
                # Equilateral triangle based on start and end position
                side = math.hypot(x2 - x1, y2 - y1)
                height = (math.sqrt(3) / 2) * side
                p1 = start_pos
                p2 = (x1 + side, y1)
                p3 = (x1 + side / 2, y1 - height)
                pygame.draw.polygon(screen, color, [p1, p2, p3], radius)

            elif current_shape == "rhombus":
                # Rhombus centered at the midpoint of start and end
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                dx = abs(x2 - x1) // 2
                dy = abs(y2 - y1) // 2
                points = [(cx, cy - dy), (cx + dx, cy), (cx, cy + dy), (cx - dx, cy)]
                pygame.draw.polygon(screen, color, points, radius)

        # Keyboard controls: change color or shape
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                color = C_RED
            if event.key == pygame.K_2:
                color = C_GREEN
            if event.key == pygame.K_3:
                color = C_BLUE
            if event.key == pygame.K_0:
                color = C_WHITE
            if event.key == pygame.K_9:
                color = C_BLACK

            if event.key == pygame.K_l:
                current_shape = "line"
            if event.key == pygame.K_s:
                current_shape = "square"
            if event.key == pygame.K_r:
                current_shape = "right_triangle"
            if event.key == pygame.K_e:
                current_shape = "equilateral_triangle"
            if event.key == pygame.K_d:
                current_shape = "rhombus"

    pygame.display.update()
    clock.tick(120)

pygame.quit()
