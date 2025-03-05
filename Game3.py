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
        self.image = transform.scale(square_image, (width, height))
        self.rect = pygame.Rect(
            x * cell_size + (cell_size - width) // 2,
            y * cell_size + (cell_size - height) // 2,
            width,
            height
        )

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


class Game_3:
    def __init__(self, exit_callback, quit_callback):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        pygame.display.set_caption("Game 3")
        self.exit = exit_callback  # Коллбек для возврата в меню
        self.quit = quit_callback  # Коллбек для выхода из игры
        self.square_image = image.load("bobr_game.png")
        self.reset_game()

    def reset_game(self):
        self.grid_size = 3
        self.cell_size = 600 // self.grid_size
        self.squares = []
        self.score = 0
        self.last_spawn_time = time.time()
        self.spawn_interval = 0.5
        self.game_over = False
        self.show_game_over_screen = False  # Флаг для отображения экрана завершения игры

    def draw_grid(self):
        for x in range(1, self.grid_size):
            pygame.draw.line(self.screen, (0, 0, 0),
                             (x * self.cell_size, 0),
                             (x * self.cell_size, 600), 2)
            pygame.draw.line(self.screen, (0, 0, 0),
                             (0, x * self.cell_size),
                             (600, x * self.cell_size), 2)

    def spawn_square(self):
        if time.time() - self.last_spawn_time > self.spawn_interval:
            self.last_spawn_time = time.time()
            occupied = [(s.x, s.y) for s in self.squares]
            available = [(x, y) for x in range(3) for y in range(3)
                         if (x, y) not in occupied]

            if available:
                x, y = random.choice(available)
                self.squares.append(Square(x, y, 70, 90,
                                           self.cell_size,
                                           self.square_image))
            else:
                self.game_over = True
                self.show_game_over_screen = True  # Показываем экран завершения игры

    def update_spawn_interval(self):
        self.spawn_interval = 0.5 - self.score // 25 * 0.05

    def handle_click(self, mouse_x, mouse_y):
        grid_x = mouse_x // self.cell_size
        grid_y = mouse_y // self.cell_size

        for square in self.squares[:]:
            if square.rect.collidepoint(mouse_x, mouse_y):
                self.squares.remove(square)
                self.score += 1

    def draw_score(self):
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Счет: {self.score}", True, (0, 0, 0))
        self.screen.blit(text, (10, 10))

    def draw_game_over_screen(self):
        self.screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 72)
        text = font.render("Игра окончена!", True, (255, 0, 0))
        text_rect = text.get_rect(center=(300, 200))
        self.screen.blit(text, text_rect)

        # Финальный счет
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Финальный счет: {self.score}", True, (0, 0, 0))
        self.screen.blit(text, (250, 250))

        # Кнопка "Заново"
        restart_btn = pygame.Rect(200, 300, 200, 50)
        pygame.draw.rect(self.screen, (0, 200, 0), restart_btn)
        text = font.render("Заново", True, (0, 0, 0))
        self.screen.blit(text, (210, 303))

        # Кнопка "Выход"
        quit_btn = pygame.Rect(200, 370, 200, 50)
        pygame.draw.rect(self.screen, (200, 0, 0), quit_btn)
        text = font.render("Выход", True, (0, 0, 0))
        self.screen.blit(text, (210, 373))

        pygame.display.flip()

        # Возвращаем координаты кнопок для обработки кликов
        return restart_btn, quit_btn

    def run(self):
        running = True
        while running:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.show_game_over_screen:
                        # Обработка кликов на экране завершения игры
                        mouse_pos = pygame.mouse.get_pos()
                        restart_btn, quit_btn = self.draw_game_over_screen()
                        if restart_btn.collidepoint(mouse_pos):
                            self.reset_game()
                            self.show_game_over_screen = False
                        elif quit_btn.collidepoint(mouse_pos):
                            self.exit()
                            running = False
                    else:
                        # Обработка кликов во время игры
                        self.handle_click(*pygame.mouse.get_pos())
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.exit()  # Возврат в главное меню
                        running = False  # Выход из игрового цикла

            # Игровая логика
            if not self.show_game_over_screen:
                self.spawn_square()
                self.update_spawn_interval()
                self.screen.fill((255, 255, 255))
                self.draw_grid()
                for square in self.squares:
                    square.draw(self.screen)
                self.draw_score()
                pygame.display.update()
                pygame.time.Clock().tick(60)
            else:
                # Отрисовка экрана завершения игры
                self.draw_game_over_screen()