import pygame
import random
import time
from pygame import Surface, image, transform

# Инициализация Pygame
pygame.init()

# Размеры экрана
screen_width = 600
screen_height = 600

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Настройки прямоугольного поля и квадрата
grid_size = 3  # 3x3 поля
cell_size = screen_width // grid_size  # Размер каждой ячейки
width = 70
height = 90
square_image = image.load("bobr_game.png")  # Создание поверхности для квадрата

class Square:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = Surface((width, height))
        self.image = square_image
        self.image = transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(x * cell_size + (cell_size - width) // 2, y * cell_size + (cell_size - height) // 2, width, height)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Button:
    def __init__(self, x, y, width, height, text, font, color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.action = action

    def draw(self, screen):
        # Рисуем кнопку
        pygame.draw.rect(screen, self.color, self.rect)
        text_surf = self.font.render(self.text, True, WHITE)
        screen.blit(text_surf, (self.rect.x + (self.rect.width - text_surf.get_width()) // 2,
                               self.rect.y + (self.rect.height - text_surf.get_height()) // 2))

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.is_hovered(pygame.mouse.get_pos()):
            if self.action:
                self.action()


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Game3")
        self.clock = pygame.time.Clock()
        self.score = 0
        self.squares = []
        self.last_spawn_time = time.time()
        self.spawn_interval = 0.3  # Интервал для появления нового квадрата в секундах
        self.game_over = False  # Флаг окончания игры
        self.font = pygame.font.SysFont(None, 36)
        self.quit_button = Button(screen_width // 2 - 100, screen_height // 2 + 50, 200, 50, "Выход", self.font, BLACK, self.quit_game)

    def draw_grid(self):
        # Рисуем сетку
        for x in range(1, grid_size):
            pygame.draw.line(self.screen, BLACK, (x * cell_size, 0), (x * cell_size, screen_height), 2)
            pygame.draw.line(self.screen, BLACK, (0, x * cell_size), (screen_width, x * cell_size), 2)

    def spawn_square(self):
        # Появление новых квадратов
        if time.time() - self.last_spawn_time > self.spawn_interval and not self.game_over:
            self.last_spawn_time = time.time()

            # Находим свободные клетки
            occupied_cells = [(square.x, square.y) for square in self.squares]
            available_cells = [(x, y) for x in range(grid_size) for y in range(grid_size) if (x, y) not in occupied_cells]

            if available_cells:
                spawn_x, spawn_y = random.choice(available_cells)
                self.squares.append(Square(spawn_x, spawn_y))
            else:
                self.game_over = True  # Все клетки заняты, игра заканчивается

    def check_square_click(self, mouse_x, mouse_y):
        # Проверяем, попали ли на квадрат
        for square in self.squares:
            if square.rect.collidepoint(mouse_x, mouse_y):
                self.squares.remove(square)  # Убираем квадрат из списка
                self.score += 1  # Увеличиваем счетчик

    def display_score(self):
        # Отображаем счет
        score_text = self.font.render(f"Счет: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

    def display_game_over(self):
        # Отображаем сообщение о завершении игры
        font = pygame.font.SysFont(None, 48)
        game_over_text = font.render("Игра окончена!", True, BLACK)
        score_text = font.render(f"Финальный счет: {self.score}", True, BLACK)
        self.screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 50))
        self.screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2 + 10))
        # Рисуем кнопку выхода
        self.quit_button.draw(self.screen)

    def quit_game(self):
        pygame.quit()
        exit()

    def update(self):
        self.screen.fill(WHITE)
        self.spawn_square()

        # Рисуем сетку
        self.draw_grid()

        # Рисуем квадраты
        for square in self.squares:
            square.draw(self.screen)

        # Отображаем счет
        self.display_score()

        # Если игра окончена, отображаем сообщение
        if self.game_over:
            self.display_game_over()

        # Обновляем экран
        pygame.display.update()

    def run(self):
        running = True
        while running:
            self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    # Получаем координаты мыши
                    mouse_x, mouse_y = pygame.mouse.get_pos()

                    # Проверка попадания по квадрату
                    self.check_square_click(mouse_x, mouse_y)

                # Обработка кнопки выхода
                if self.game_over:
                    self.quit_button.handle_event(event)

            # Обновление состояния игры
            self.update()

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
