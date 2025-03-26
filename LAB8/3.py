import pygame
import math

pygame.init()

# Window dimensions
WIDTH = 800
HEIGHT = 600

# Screen and "base layer" where drawn shapes are stored
screen = pygame.display.set_mode((WIDTH, HEIGHT))
base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill((255, 255, 255))  # Fill with white background

# Colors
colorRED = (255, 0, 0)
colorBLACK = (0, 0, 0)
colorWHITE = (255, 255, 255)

clock = pygame.time.Clock()

# State variables
LMBpressed = False
THICKNESS = 5

# Mouse coordinates
currX = 0
currY = 0
prevX = 0
prevY = 0

# Shape mode (default is rectangle)
shape_mode = 'rect'

# Function to calculate a rectangle from two points
def calculate_rect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

# Function to draw the selected shape
def draw_shape(surf, shape, x1, y1, x2, y2, color, thickness):
    if shape == 'rect':
        pygame.draw.rect(surf, color, calculate_rect(x1, y1, x2, y2), thickness)

    elif shape == 'square':
        side = min(abs(x2 - x1), abs(y2 - y1))
        rect = pygame.Rect(x1, y1, side, side)
        pygame.draw.rect(surf, color, rect, thickness)

    elif shape == 'right_triangle':
        points = [(x1, y1), (x2, y2), (x1, y2)]
        pygame.draw.polygon(surf, color, points, thickness)

    elif shape == 'equilateral_triangle':
        side = abs(x2 - x1)
        height = int((math.sqrt(3) / 2) * side)
        points = [(x1, y1), (x1 + side, y1), (x1 + side // 2, y1 - height)]
        pygame.draw.polygon(surf, color, points, thickness)

    elif shape == 'rhombus':
        dx = abs(x2 - x1) // 2
        dy = abs(y2 - y1) // 2
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        points = [(cx, y1), (x2, cy), (cx, y2), (x1, cy)]
        pygame.draw.polygon(surf, color, points, thickness)

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Left mouse button press - start drawing
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMBpressed = True
            prevX, prevY = event.pos

        # Mouse movement while holding LMB - shape preview
        if event.type == pygame.MOUSEMOTION and LMBpressed:
            currX, currY = event.pos
            screen.blit(base_layer, (0, 0))  # Display previously drawn shapes
            draw_shape(screen, shape_mode, prevX, prevY, currX, currY, colorRED, THICKNESS)

        # Releasing LMB - save the shape
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False
            currX, currY = event.pos
            draw_shape(screen, shape_mode, prevX, prevY, currX, currY, colorRED, THICKNESS)
            base_layer.blit(screen, (0, 0))  # Save the drawn shapes

        # Keyboard controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:
                THICKNESS += 1
            if (event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS) and THICKNESS > 1:
                THICKNESS -= 1

            # Switch shapes
            if event.key == pygame.K_0:
                shape_mode = 'rect'
            if event.key == pygame.K_1:
                shape_mode = 'square'
            if event.key == pygame.K_2:
                shape_mode = 'right_triangle'
            if event.key == pygame.K_3:
                shape_mode = 'equilateral_triangle'
            if event.key == pygame.K_4:
                shape_mode = 'rhombus'

            # Clear screen with C key
            if event.key == pygame.K_c:
                base_layer.fill(colorWHITE)

    # Display update
    pygame.display.flip()
    clock.tick(60)
