import pygame
import sys
from Game1 import Game_1, Coin, SpawnPoint, meteor
from Game2 import game_2
from Game3 import game_3
from Button_file import Button

# Инициализация Pygame
pygame.init()

# Размеры экрана
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Главное меню")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)

logo_image = pygame.image.load("logo_bobr_game.png")  # Путь к вашему логотипу (например, 'logo.png')
logo_width = 400  # Новая ширина
logo_height = int(logo_image.get_height() * (logo_width / logo_image.get_width()))  # Сохраняем пропорции
logo_image = pygame.transform.scale(logo_image, (logo_width, logo_height))  # Масштабируем изображение
logo_rect = logo_image.get_rect(center=(WIDTH // 2, 100))  # Размещаем логотип в центре по горизонтали и на 100 пикселей сверху

# Функции для игр
def start_game_1():
    game_1 = Game_1()
    game_1.run()


def start_game_2():
    game_2()


def start_game_3():
    game_3()


def exit_game():
    pygame.quit()
    sys.exit()


# Главная функция для отображения меню
def main_menu():
    # Создание кнопок
    buttons = [
        Button("Игра 1", 300, 180, 200, 50, start_game_1),
        Button("Игра 2", 300, 250, 200, 50, start_game_2),
        Button("Игра 3", 300, 320, 200, 50, start_game_3),
        Button("Выход", 300, 390, 200, 50, exit_game)
    ]

    # Главный цикл меню
    while True:
        screen.fill(WHITE)

        screen.blit(logo_image, logo_rect)

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game()
            if event.type == pygame.MOUSEBUTTONDOWN: 
                if event.button == 1:  # Левый клик мыши
                    for button in buttons:
                        if button.is_hovered(pygame.mouse.get_pos()):
                            button.click()

        # Отображаем кнопки
        for button in buttons:
            button.draw(screen)

        # Отображаем информацию
        pygame.display.flip()


# Запуск основного меню
if __name__ == "__main__":
    main_menu()
