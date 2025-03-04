import pygame
from pygame import *
from random import randint
import sys

FPS = 60
Frames = pygame.time.Clock()
WIDTH = 40
HEIGHT = 70
WIN_WIDTH = 400  # Ширина окна
WIN_HEIGHT = 640  # Высота окна
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = (70, 195, 219)

class Bobr:
    def __init__(self):
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
            return True
        return False

    def update(self):
        self.rect.move_ip(0, self.velocity)
        self.velocity += self.gravity
        self.key_press()


class Pipe:
    def __init__(self):
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
        self.rect_top.move_ip(self.speed, 0)
        self.rect_bottom.move_ip(self.speed, 0)
        if self.rect_top.right < 0:
            self.image_top = pygame.transform.smoothscale(self.image_top, (self.width, self.random_height()))
            self.rect_top = self.image_top.get_rect()
            self.rect_top.right = WIN_WIDTH + self.width
            self.image_bottom = pygame.transform.smoothscale(self.image_bottom, (self.width, self.random_height()))
            self.rect_bottom = self.image_bottom.get_rect()
            self.rect_bottom.bottom = WIN_HEIGHT + 10
            self.rect_bottom.right = WIN_WIDTH + self.width

    def draw(self, surface):
        surface.blit(self.image_top, self.rect_top)
        surface.blit(self.image_bottom, self.rect_bottom)


class Game_2:
    def __init__(self, exit_callback, quit_callback):
        pygame.init()
        self.screen = pygame.display.set_mode(DISPLAY)
        pygame.display.set_caption('Game 2')
        self.exit = exit_callback
        self.quit = quit_callback
        self.bobr = Bobr()
        self.pipe = Pipe()
        self.status = True

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.quit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.exit()
                        return

            if self.status:
                self.bobr.update()
                self.pipe.update()
                if self.bobr.check_collision(self.pipe):
                    self.status = False

            self.screen.fill(BACKGROUND_COLOR)
            self.bobr.draw(self.screen)
            self.pipe.draw(self.screen)

            if not self.status:
                font = pygame.font.Font(None, 72)
                text = font.render("Game Over", True, (255, 0, 0))
                self.screen.blit(text, (WIN_WIDTH // 2 - 140, WIN_HEIGHT // 2 - 50))

            pygame.display.update()
            Frames.tick(FPS)