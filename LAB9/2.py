import pygame
import random
import time

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Define colors
Red = (255, 0, 0)
White = (255, 255, 255)
Black = (0, 0, 0)
Gray = (128, 128, 128)
Blue = (0, 0, 255)
Green = (0, 255, 0)
Yellow = (255, 255, 0)

# Screen and grid settings
Height = 800
Width = 800
FPS = 7
Cell = 30


# Create screen
screen = pygame.display.set_mode((Height, Width))

# Initial score
score = 0

# Draw grid on screen
def draw_grid():
    for i in range(Width // Cell):
        for j in range(Height // Cell):
            pygame.draw.rect(screen, Gray, (i * Cell, j * Cell, Cell, Cell), 1)

# Show game over or win message
def show_message(text, color, size):
    font = pygame.font.SysFont("Arial", size, bold=True)
    render = font.render(text, True, color)
    rect = render.get_rect(center=(Width // 2, Height // 2))
    screen.blit(render, rect)
    pygame.display.flip()

# Show score in top-left
def show_score(score):
    font = pygame.font.SysFont("Arial", 30)
    text = font.render(f"Score: {score}", True, Black)
    screen.blit(text, (10, 10))

# Point class for positions
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Snake class
class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        self.body[0].x += self.dx
        self.body[0].y += self.dy

        # Teleport from edges (toroidal)
        if self.body[0].x >= Width // Cell:
            self.body[0].x = 0
        elif self.body[0].x < 0:
            self.body[0].x = Width // Cell - 1
        if self.body[0].y >= Height // Cell:
            self.body[0].y = 0
        elif self.body[0].y < 0:
            self.body[0].y = Height // Cell - 1

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, Red, (head.x * Cell, head.y * Cell, Cell, Cell))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, Blue, (segment.x * Cell, segment.y * Cell, Cell, Cell))

    def check_coll(self, food):
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            self.body.append(Point(head.x, head.y))
            food.generate_random()
            return food.weight
        return 0

    def selfcoll(self):
        head = self.body[0]
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True
        return False

# Food class
class Food:
    def __init__(self):
        self.pos = Point(9, 9)
        self.weight = 1
        self.last_spawn_time = time.time()

    def draw(self):
        if self.weight == 1:
            color = Green
        elif self.weight == 2:
            color = Yellow
        else:
            color = Red
        pygame.draw.rect(screen, color, (self.pos.x * Cell, self.pos.y * Cell, Cell, Cell))

    def generate_random(self):
        self.pos.x = random.randint(0, Width // Cell - 1)
        self.pos.y = random.randint(0, Height // Cell - 1)
        self.weight = random.choice([1, 2, 3])
        self.last_spawn_time = time.time()

    def check_timeout(self, timeout_seconds=5):
        if time.time() - self.last_spawn_time > timeout_seconds:
            self.generate_random()

# Game initialization
s = Snake()
f = Food()
running = True
clock = pygame.time.Clock()

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and s.dx != -1:
                s.dx = 1
                s.dy = 0
            elif event.key == pygame.K_LEFT and s.dx != 1:
                s.dx = -1
                s.dy = 0
            elif event.key == pygame.K_DOWN and s.dy != -1:
                s.dx = 0
                s.dy = 1
            elif event.key == pygame.K_UP and s.dy != 1:
                s.dx = 0
                s.dy = -1

    # Check self collision (Game over)
    if s.selfcoll():
        running = False
        pygame.mixer.music.play()
        show_message(f"You lost! Score: {score}", Red, 72)
        pygame.time.delay(3000)
        break

    # Update screen and game state
    screen.fill(White)

    # Check if food timed out
    f.check_timeout(timeout_seconds=5)

    # Snake eats food
    gain = s.check_coll(f)
    score += gain
    if gain:
        FPS += 1

    draw_grid()
    show_score(score)
    s.draw()
    f.draw()
    pygame.display.flip()
    s.move()
    clock.tick(FPS)
