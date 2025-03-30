import pygame
import sys
import random

pygame.init()

# Game window dimensions
HEIGHT = 600
WIDTH = 600

# Grid configuration
grid_SIZE = 20 
grid_WIDTH = WIDTH // grid_SIZE
grid_HEIGHT = HEIGHT // grid_SIZE

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Initialize screen and clock
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
surface = pygame.Surface(screen.get_size())
surface = surface.convert()

# Food timeout in milliseconds
FOOD_TIMEOUT = 5000

# Function to draw background grid with new green colors
def drawGrid(surface):
    for y in range(0, grid_HEIGHT):
        for x in range(0, grid_WIDTH): 
            r = pygame.Rect((x * grid_SIZE, y * grid_SIZE), (grid_SIZE, grid_SIZE))
            if (x + y) % 2 == 0:
                pygame.draw.rect(surface, (170, 215, 81), r)   # Light green
            else:
                pygame.draw.rect(surface, (162, 209, 73), r)   # Dark green

# Snake class
class Snake(object):
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]  # Start at center
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (17, 24, 47)  # Snake color (dark blue)

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        # Prevent the snake from reversing into itself
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def move(self):
        # Calculate new head position
        cur = self.get_head_position()
        x, y = self.direction
        new = (((cur[0] + (x * grid_SIZE)) % WIDTH), (cur[1] + (y * grid_SIZE)) % HEIGHT)

        # Collision with self resets the snake
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    def reset(self):
        # Restart snake from center
        self.length = 1
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def draw(self, surface):
        # Draw snake segments
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (grid_SIZE, grid_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (93, 216, 228), r, 1)  # Border color

    def handle_keys(self):
        # Handle user input (arrow keys)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                elif event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                elif event.key == pygame.K_LEFT:  
                    self.turn(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

# Food class with weight
class Food(object):
    def __init__(self):
        self.color = (223, 163, 49)  # Orange
        self.randomize_position()

    def randomize_position(self):
        # Random position and random weight (1–3)
        self.position = (random.randint(0, grid_WIDTH - 1) * grid_SIZE,
                         random.randint(0, grid_HEIGHT - 1) * grid_SIZE)
        self.weight = random.randint(1, 3)
        self.spawn_time = pygame.time.get_ticks()

    def draw(self, surface):
        # Draw food square
        r = pygame.Rect((self.position[0], self.position[1]), (grid_SIZE, grid_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (93, 216, 228), r, 1)  # Border
        # Show the weight as number
        font = pygame.font.SysFont("monospace", 16)
        text = font.render(str(self.weight), True, (0, 0, 0))
        text_rect = text.get_rect(center=r.center)
        surface.blit(text, text_rect)

# Game setup
snake = Snake()
food = Food()
FPS = 5
score = 0
myfont = pygame.font.SysFont("monospace", 16)

# Main game loop
while True:
    snake.handle_keys()
    drawGrid(surface)
    snake.move()

    # Remove and respawn food if too old
    if pygame.time.get_ticks() - food.spawn_time > FOOD_TIMEOUT:
        food.randomize_position()

    # Check for food collision
    if snake.get_head_position() == food.position:
        snake.length += food.weight
        score += food.weight
        FPS += food.weight  # Speed increases based on food weight
        food.randomize_position()

    snake.draw(surface)
    food.draw(surface)
    
    # Draw everything
    screen.blit(surface, (0, 0))
    text = myfont.render("Score: {0}".format(score), 1, (0, 0, 0))
    screen.blit(text, (5, 10))
    
    pygame.display.flip()
    clock.tick(FPS)
