import pygame
import random
import time
from pygame import Surface, image, transform

# Инициализация Pygame
pygame.init()

# Размеры экрана
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("GameTest")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Настройки прямоугольного поля и квадрата
grid_size = 3  # 3x3 поля
cell_size = screen_width // grid_size  # Размер каждой ячейки
square_size = 50  # Размер квадрата
square_image = image.load("bobr_game.png")  # Создание поверхности для квадрата

# Класс для квадрата
class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = Surface((square_size, square_size))
        self.image = square_image
        self.image = transform.scale(self.image, (square_size, square_size))
        self.rect = pygame.Rect(x * cell_size + (cell_size - square_size) // 2, y * cell_size + (cell_size - square_size) // 2, square_size, square_size)

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

# Главная функция игры
def game_loop():
    running = True
    clock = pygame.time.Clock()

    score = 0
    squares = []
    last_spawn_time = time.time()
    spawn_interval = 1  # Интервал для появления нового квадрата в секундах

    while running:
        screen.fill(WHITE)

        # Проверка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Получаем координаты мыши
                mouse_x, mouse_y = pygame.mouse.get_pos()
                grid_x = mouse_x // cell_size
                grid_y = mouse_y // cell_size

                # Проверяем, попали ли на квадрат
                for square in squares:
                    if square.rect.collidepoint(mouse_x, mouse_y):
                        squares.remove(square)  # Убираем квадрат из списка
                        score += 1  # Увеличиваем счетчик

        # Появление новых квадратов
        if time.time() - last_spawn_time > spawn_interval:
            last_spawn_time = time.time()

            # Находим свободные клетки
            occupied_cells = [(square.x, square.y) for square in squares]
            available_cells = [(x, y) for x in range(grid_size) for y in range(grid_size) if (x, y) not in occupied_cells]

            if available_cells:
                spawn_x, spawn_y = random.choice(available_cells)
                squares.append(Square(spawn_x, spawn_y))
            else:
                pygame.quit()

        # Рисуем сетку
        for x in range(1, grid_size):
            pygame.draw.line(screen, BLACK, (x * cell_size, 0), (x * cell_size, screen_height), 2)
            pygame.draw.line(screen, BLACK, (0, x * cell_size), (screen_width, x * cell_size), 2)

        # Рисуем квадраты
        for square in squares:
            square.draw()

        # Отображаем счет
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Счет: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

# Запуск игры
if __name__ == "__main__":
    game_loop()
