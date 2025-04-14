import pygame
import sys
import random
import time
import psycopg2

# ----------- Подключение к базе данных PostgreSQL -----------
conn = psycopg2.connect(
    database="SnakeGame",
    user="postgres",
    password="20062008",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# ----------- Ввод имени пользователя -----------
username = input("Введите имя пользователя: ")

# ----------- Поиск или создание пользователя -----------
cur.execute("SELECT id FROM users WHERE username = %s", (username,))
user = cur.fetchone()

if user:
    user_id = user[0]
    print(f"🎮 Добро пожаловать, {username}! Ваш ID: {user_id}")

    cur.execute(
        "SELECT score, level, saved_at FROM user_score WHERE user_id = %s ORDER BY saved_at DESC LIMIT 1",
        (user_id,)
    )
    last_data = cur.fetchone()
    if last_data:
        print(f"📄 Последний результат: Очки = {last_data[0]}, Уровень = {last_data[1]}, Время = {last_data[2]}")
    else:
        print("📭 Нет предыдущих результатов.")
else:
    cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
    user_id = cur.fetchone()[0]
    conn.commit()
    print(f"🆕 Новый игрок зарегистрирован: {username}, ID = {user_id}")

# ----------- Загрузка последнего состояния -----------
cur.execute("SELECT score, level FROM user_score WHERE user_id = %s ORDER BY saved_at DESC LIMIT 1", (user_id,))
last_record = cur.fetchone()
score = last_record[0] if last_record else 0
FPS = last_record[1] if last_record else 10

# ----------- Настройки игры Pygame -----------
pygame.init()
HEIGHT, WIDTH = 600, 600
grid_SIZE = 20
grid_WIDTH = WIDTH // grid_SIZE
grid_HEIGHT = HEIGHT // grid_SIZE
UP, DOWN, LEFT, RIGHT = (0, -1), (0, 1), (-1, 0), (1, 0)

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
surface = pygame.Surface(screen.get_size()).convert()
myfont = pygame.font.SysFont("Arial", 20)

# ----------- Отрисовка сетки -----------
def drawGrid(surface):
    for y in range(grid_HEIGHT):
        for x in range(grid_WIDTH):
            r = pygame.Rect((x * grid_SIZE, y * grid_SIZE), (grid_SIZE, grid_SIZE))
            color = (170, 215, 81) if (x + y) % 2 == 0 else (162, 209, 73)
            pygame.draw.rect(surface, color, r)

# ----------- Класс Змеи -----------
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH // 2), (HEIGHT // 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (0, 0, 255)
        self.dead = False

    def get_head_position(self):
        return self.positions[0]

    def turn(self, point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        self.direction = point

    def move(self):
        if self.dead:
            return
        cur = self.get_head_position()
        x, y = self.direction
        new = (cur[0] + x * grid_SIZE, cur[1] + y * grid_SIZE)

        if new[0] < 0 or new[0] >= WIDTH or new[1] < 0 or new[1] >= HEIGHT or new in self.positions[2:]:
            self.dead = True
            return

        self.positions.insert(0, new)
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        self.__init__()

    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (grid_SIZE, grid_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (0, 0, 0), r, 1)

# ----------- Класс Еды -----------
class Food:
    def __init__(self):
        self.color = (255, 0, 0)
        self.position = (0, 0)
        self.weight = 1
        self.spawn_time = 0
        self.randomize_position()

    def randomize_position(self):
        self.position = (random.randint(0, grid_WIDTH - 1) * grid_SIZE,
                         random.randint(0, grid_HEIGHT - 1) * grid_SIZE)
        self.weight = random.randint(1, 3)
        self.spawn_time = time.time()

    def is_expired(self):
        return time.time() - self.spawn_time > 3

    def draw(self, surface):
        r = pygame.Rect(self.position, (grid_SIZE, grid_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (0, 0, 0), r, 1)

# ----------- Инициализация игры -----------
snake = Snake()
food = Food()
death_count = 0

# ----------- Игровой цикл -----------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            cur.close()
            conn.close()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.turn(UP)
            elif event.key == pygame.K_DOWN:
                snake.turn(DOWN)
            elif event.key == pygame.K_LEFT:
                snake.turn(LEFT)
            elif event.key == pygame.K_RIGHT:
                snake.turn(RIGHT)
            elif event.key == pygame.K_p:
                # Сохранение текущего состояния в БД
                cur.execute(
                    "INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s)",
                    (user_id, score, FPS)
                )
                conn.commit()
                print(f"💾 Игра сохранена: очки = {score}, уровень = {FPS}")

    if snake.dead:
        death_count += 1
        surface.fill((255, 0, 0))
        screen.blit(surface, (0, 0))
        screen.blit(myfont.render("ИГРА ОКОНЧЕНА!", True, (0, 0, 0)), (WIDTH // 2 - 80, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)

        if death_count == 2:
            # Автоматическое сохранение после второй смерти
            cur.execute(
                "INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s)",
                (user_id, score, FPS)
            )
            conn.commit()
            print(f"🎮 Состояние автоматически сохранено: очки = {score}, уровень = {FPS}")
            pygame.quit()
            cur.close()
            conn.close()
            sys.exit()

        snake.reset()
        food.randomize_position()
        score = 0
        FPS = 10
        continue

    drawGrid(surface)
    snake.move()

    if snake.get_head_position() == food.position:
        snake.length += food.weight
        score += food.weight
        FPS += 1
        food.randomize_position()

    if food.is_expired():
        food.randomize_position()

    snake.draw(surface)
    food.draw(surface)
    screen.blit(surface, (0, 0))

    # ----------- Отображение информации в интерфейсе -----------
    screen.blit(myfont.render(f"Игрок: {username}", True, (0, 0, 0)), (5, 10))
    screen.blit(myfont.render(f"Очки: {score}", True, (0, 0, 0)), (5, 30))
    screen.blit(myfont.render(f"Уровень (скорость): {FPS}", True, (0, 0, 0)), (5, 50))
    screen.blit(myfont.render("Нажмите P — пауза и сохранение", True, (0, 0, 0)), (5, 70))

    pygame.display.flip()
    clock.tick(FPS)
