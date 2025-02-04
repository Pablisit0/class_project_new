import pygame
import random

# Инициализация Pygame
pygame.init()

# Определяем размеры экрана и создаем окно
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Meteorites and Platforms with Coins")

# Определяем цвета
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Задаем параметры игры
clock = pygame.time.Clock()
FPS = 60
GRAVITY = 1
JUMP_STRENGTH = 20

# Платформы
platforms = [
    pygame.Rect(100, 500, 600, 20),
    pygame.Rect(200, 400, 300, 20),
    pygame.Rect(400, 300, 200, 20)
]

# Игрок
player = pygame.Rect(50, 450, 50, 50)
player_vel_y = 0
is_jumping = False

# Метеориты
meteorites = []
meteor_timer = 0

# Монетки
coins = []
coin_count = 0

def spawn_meteor():
    x = random.randint(0, WIDTH - 30)
    meteorites.append(pygame.Rect(x, 0, 30, 30))

def spawn_coin():
    x = random.randint(50, WIDTH - 50)
    y = random.randint(50, HEIGHT - 50)
    coins.append(pygame.Rect(x, y, 20, 20))

# Основной игровой цикл
running = True

# Создаем начальные монетки
for _ in range(5):
    spawn_coin()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.x -= 5
    if keys[pygame.K_RIGHT]:
        player.x += 5
    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True
        player_vel_y = -JUMP_STRENGTH

    # Применяем гравитацию
    if is_jumping:
        player_vel_y += GRAVITY
        player.y += player_vel_y

    # Проверяем столкновение с платформами
    for plat in platforms:
        if player.colliderect(plat) and player_vel_y >= 0:  # Проверка на столкновение при падении
            player.y = plat.top - player.height
            player_vel_y = 0
            is_jumping = False

    # Проверка столкновения с метеоритами
    for meteor in meteorites:
        if player.colliderect(meteor):
            print("Game Over!")
            running = False

    # Проверка столкновения с монетками
    for coin in coins[:]:  # Используем копию списка, чтобы изменять оригинал
        if player.colliderect(coin):
            coins.remove(coin)  # Удаляем монетку
            coin_count += 1  # Увеличиваем счетчик монеток

    # Генерация метеоритов
    meteor_timer += 1
    if meteor_timer > 30:  # Каждые 30 кадров
        spawn_meteor()
        meteor_timer = 0

    # Обновляем позиции метеоритов
    for meteor in meteorites:
        meteor.y += 5  # Метеориты падают со скоростью 5
        if meteor.y > HEIGHT:
            meteorites.remove(meteor)  # Удаляем метеориты за пределами экрана

    # Отображение на экране
    screen.fill(WHITE)

    # Рисуем платформы
    for plat in platforms:
        pygame.draw.rect(screen, BLUE, plat)

    # Рисуем игрока
    pygame.draw.rect(screen, GREEN, player)

    # Рисуем метеориты
    for meteor in meteorites:
        pygame.draw.rect(screen, RED, meteor)

    # Рисуем монетки
    for coin in coins:
        pygame.draw.rect(screen, YELLOW, coin)

    # Отображаем счетчик монеток
    font = pygame.font.Font(None, 36)
    text = font.render(f"Coins: {coin_count}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()