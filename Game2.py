import pygame
from pygame import *
from random import randint
import sys
from Button_file import Button

FPS = 60
Frames = pygame.time.Clock()
WIDTH = 40
HEIGHT = 70
WIN_WIDTH = 400  # Ширина создаваемого окна
WIN_HEIGHT = 640  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = (70, 195, 219)

class Bobr:
    def __init__(self, game):
        self.game = game  # Сохраняем ссылку на объект игры
        self.image = pygame.image.load("bobr_game.png")
        self.image = transform.scale(self.image, (WIDTH, HEIGHT))
        self.rect = self.image.get_rect()
        self.rect.top = WIDTH / 2 - self.rect.height / 2
        self.rect.left = 20
        self.velocity = 1
        self.gravity = 0.2

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def key_press(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_SPACE]:
            self.velocity = -5

    def check_collision(self, pipe):
        if ((pipe.rect_top.left <= self.rect.right and pipe.rect_top.bottom >= self.rect.top)
                or (pipe.rect_bottom.left <= self.rect.right and pipe.rect_bottom.top <= self.rect.bottom)
                or (self.rect.bottom >= WIN_HEIGHT) or (self.rect.bottom <= 0)):
            self.game.end_game()  # Вызов метода end_game() через объект game

    def update(self):
        self.rect.move_ip(0, self.velocity)
        self.velocity += self.gravity
        self.key_press()


class Pipe:
    def __init__(self):
        # Базовые свойства
        self.width = 50
        self.height = 200
        self.speed = -2
        # Верхнее препятствие
        self.image_top = pygame.image.load('pipe.png')
        self.image_top = pygame.transform.rotate(self.image_top, 180)
        self.image_top = pygame.transform.smoothscale(self.image_top, (self.width, self.height))
        self.rect_top = self.image_top.get_rect()
        self.rect_top.top = -10
        self.rect_top.right = WIN_WIDTH + self.width
        # Нижнее препятствие
        self.image_bottom = pygame.image.load('pipe.png')
        self.image_bottom = pygame.transform.smoothscale(self.image_bottom, (self.width, self.height))
        self.rect_bottom = self.image_bottom.get_rect()
        self.rect_bottom.bottom = WIN_HEIGHT + 10
        self.rect_bottom.right = WIN_WIDTH + self.width

    def random_height(self):
        return randint(200, 240)

    def update(self):
        # Верхнее препятствие
        self.rect_top.move_ip(self.speed, 0)
        # Нижнее препятствие
        self.rect_bottom.move_ip(self.speed, 0)
        if self.rect_top.right < 0:
            # Верхнее препятствие
            self.image_top = pygame.transform.smoothscale(self.image_top, (self.width, self.random_height()))
            self.rect_top = self.image_top.get_rect()
            self.rect_top.right = WIN_WIDTH + self.width
            # Нижнее препятствие
            self.image_bottom = pygame.transform.smoothscale(self.image_bottom, (self.width, self.random_height()))
            self.rect_bottom = self.image_bottom.get_rect()
            self.rect_bottom.bottom = WIN_HEIGHT + 10
            self.rect_bottom.right = WIN_WIDTH + self.width

    def draw(self, surface):
        # Верхнее препятствие
        surface.blit(self.image_top, self.rect_top)
        # Нижнее препятствие
        surface.blit(self.image_bottom, self.rect_bottom)


class Game:
    def __init__(self, exit_to_menu_callback, quit_callback):
        self.exit_to_menu_callback = exit_to_menu_callback  # Функция для возврата в меню
        self.quit_callback = quit_callback  # Функция для выхода из игры
        self.status = True
        self.bobr = Bobr(self)  # Передаем ссылку на объект игры в Bobr
        self.pipe = Pipe()

    def get_status(self):
        return self.status

    def end_game(self):
        self.status = False

    def end_title(self, surface):
        Button("Заново", 200, WIN_HEIGHT // 2, 150, 50, self.restart)
        Button("Выход в меню", 200, WIN_HEIGHT // 2 + 70, 150, 50, self.exit_to_menu_callback)
        text_color = (254, 255, 137)
        bg_color = (48, 58, 82)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Конец игры', True, text_color, bg_color)
        text_rect = text.get_rect()
        text_rect.center = (WIN_WIDTH // 2, WIN_HEIGHT // 2)
        surface.blit(text, text_rect)

    def restart(self):
        self.__init__(self.exit_to_menu_callback, self.quit_callback)
        self.run()

    def update(self):
        self.bobr.update()
        self.pipe.update()
        self.bobr.check_collision(self.pipe)

    def draw(self, surface):
        self.bobr.draw(surface)
        self.pipe.draw(surface)


class Game_2:
    def __init__(self, exit_to_menu_callback, quit_callback):
        pygame.init()
        pygame.display.set_caption('Game2')
        self.screen_surface = pygame.display.set_mode(DISPLAY)
        self.game = Game(exit_to_menu_callback, quit_callback)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.game.quit_callback()

            if self.game.get_status():
                self.game.update()

            self.screen_surface.fill(BACKGROUND_COLOR)
            self.game.draw(self.screen_surface)
            if not self.game.get_status():
                self.game.end_title(self.screen_surface)

            pygame.display.update()
            Frames.tick(FPS)
