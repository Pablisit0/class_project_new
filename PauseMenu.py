import pygame
import sys

from Button_file import Button
from MainMenu import main_menu
from Game1 import game_1

# Инициализация Pygame
pygame.init()

# Размеры экрана
WIDTH, HEIGHT = 800, 600
sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Меню Паузы")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)

class PauseMenu:
    def __init__(self, game, menu):
        self.game = game
        self.menu = menu

    def start_game(self, game):
        game()

    def return_to_main_menu(self, menu):
        menu()

    # Главная функция для отображения меню
    def pause_menu(self, game, menu):
        # Создание кнопок
        b = [
            Button("Вернуться на главную", 150, 180, 500, 50, menu),
            Button("Продолжить", 250, 250, 250, 50, game)
        ]

        while True:
            sc.fill(BLACK)

            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Левый клик мыши
                        for button in b:
                            if button.is_hovered(pygame.mouse.get_pos()):
                                button.click()

            # Отображаем кнопки
            for button in b:
                button.draw(sc)

            # Отображаем информацию
            pygame.display.flip()
