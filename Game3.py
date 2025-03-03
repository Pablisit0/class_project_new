import pygame
import random
import time
from pygame import Surface, image, transform

class Square:
    def __init__(self, x, y, width, height, cell_size, square_image):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.image = Surface((width, height))
        self.image = square_image
        self.image = transform.scale(self.image, (width, height))
        self.rect = pygame.Rect(x * cell_size + (cell_size - width) // 2,
                                y * cell_size + (cell_size - height) // 2, width, height)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))


class Game_3:
    def __init__(self, exit_to_menu_callback, quit_callback):
        pygame.init()
        self.exit_to_menu_callback = exit_to_menu_callback  # Функция для возврата в меню
        self.quit_callback = quit_callback  # Функция для выхода из игры

        self.screen_width = 600
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Game3")

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)

        self.grid_size = 3
        self.cell_size = self.screen_width // self.grid_size
        self.width = 70
        self.height = 90
        self.square_image = image.load("bobr_game.png")

        self.squares = []
        self.score = 0
        self.last_spawn_time = time.time()
        self.spawn_interval = 0.3  # Интервал для появления нового квадрата в секундах

        self.clock = pygame.time.Clock()

    def draw_grid(self):
        for x in range(1, self.grid_size):
            pygame.draw.line(self.screen, self.BLACK, (x * self.cell_size, 0), (x * self.cell_size, self.screen_height),
                             2)
            pygame.draw.line(self.screen, self.BLACK, (0, x * self.cell_size), (self.screen_width, x * self.cell_size),
                             2)

    def draw_score(self):
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Счет: {self.score}", True, self.BLACK)
        self.screen.blit(score_text, (10, 10))

    def spawn_square(self):
        if time.time() - self.last_spawn_time > self.spawn_interval:
            self.last_spawn_time = time.time()

            occupied_cells = [(square.x, square.y) for square in self.squares]
            available_cells = [(x, y) for x in range(self.grid_size) for y in range(self.grid_size) if
                               (x, y) not in occupied_cells]

            if available_cells:
                spawn_x, spawn_y = random.choice(available_cells)
                self.squares.append(
                    Square(spawn_x, spawn_y, self.width, self.height, self.cell_size, self.square_image))
            else:
                pygame.quit()

    def handle_mouse_click(self, mouse_x, mouse_y):
        grid_x = mouse_x // self.cell_size
        grid_y = mouse_y // self.cell_size

        for square in self.squares:
            if square.rect.collidepoint(mouse_x, mouse_y):
                self.squares.remove(square)
                self.score += 1

    def update_spawn_interval(self):
        self.spawn_interval = 0.5 - self.score // 25 * 0.05

    def run(self):
        running = True
        while running:
            self.screen.fill(self.WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.quit_callback()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    self.handle_mouse_click(mouse_x, mouse_y)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Выход в меню по нажатию ESC
                        self.exit_to_menu_callback()
                        return

            self.spawn_square()
            self.update_spawn_interval()

            self.draw_grid()
            for square in self.squares:
                square.draw(self.screen)

            self.draw_score()

            pygame.display.update()
            self.clock.tick(60)

        pygame.quit()
