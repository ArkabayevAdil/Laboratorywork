import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set screen size
HEIGHT = 600
WIDTH = 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load image resources
road = pygame.image.load("resources/AnimatedStreet.png")
coin_i = pygame.image.load("resources/coin.png")
coin_im = pygame.transform.scale(coin_i, (100, 100))
player_im = pygame.image.load("resources/Player.png")
enemy_im = pygame.image.load("resources/Enemy.png")

# Load music and sound effects
pygame.mixer.music.load("resources/background.wav")
pygame.mixer.music.play(-1)
coin_sound = pygame.mixer.Sound("resources/coin.mp3")
crash_sound = pygame.mixer.Sound("resources/crash.wav")

# Initialize font and score
font = pygame.font.SysFont("Verdana", 30)
score = 0               # Total score (based on coin weight)
coins_collected = 0     # Total coins collected (regardless of weight)

# Every N coins collected, enemy speed increases by 1
COINS_FOR_SPEEDUP = 5

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_im
        self.speed = 5
        self.rect = self.image.get_rect()
        self.rect.midbottom = (WIDTH // 2, HEIGHT - 10)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if keys[pygame.K_UP]:
            self.rect.move_ip(0, -self.speed)
        if keys[pygame.K_DOWN]:
            self.rect.move_ip(0, self.speed)

        # Prevent player from going out of bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

# Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = coin_im
        self.speed = 7
        self.rect = self.image.get_rect()
        self.weight = random.randint(1, 3)  # Coin has random weight
        self.generate()

    def generate(self):
        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.bottom = 0
        self.weight = random.randint(1, 3)  # Assign new weight when respawned

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.generate()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_im
        self.speed = 8
        self.rect = self.image.get_rect()
        self.generate()

    def generate(self):
        self.rect.left = random.randint(0, WIDTH - self.rect.width)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > HEIGHT:
            self.generate()

# Initialize objects and sprite groups
player = Player()
coin = Coin()
enemy = Enemy()

all_sprites = pygame.sprite.Group(player, coin, enemy)
coin_sprites = pygame.sprite.Group(coin)
enemy_sprites = pygame.sprite.Group(enemy)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    player.move()
    coin.move()
    enemy.move()

    # Player collects a coin
    if pygame.sprite.spritecollideany(player, coin_sprites):
        coin_sound.play()
        score += coin.weight              # Score increases by coin weight
        coins_collected += 1             # Track how many coins collected
        coin.generate()

        # Increase enemy speed every N coins
        if coins_collected % COINS_FOR_SPEEDUP == 0:
            enemy.speed += 1

    # Player collides with enemy: Game Over
    if pygame.sprite.spritecollideany(player, enemy_sprites):
        crash_sound.play()
        pygame.time.delay(1000)
        screen.fill((255, 0, 0))
        game_over_text = font.render("Game Over!", True, (0, 0, 0))
        screen.blit(game_over_text, (WIDTH // 2 - 80, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()

    # Draw game screen
    screen.blit(road, (0, 0))
    all_sprites.draw(screen)

    # Show score
    score_text = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    # Show enemy speed (optional)
    speed_text = font.render(f"Enemy Speed: {enemy.speed}", True, (0, 0, 0))
    screen.blit(speed_text, (10, 50))

    pygame.display.flip()
    clock.tick(60)
