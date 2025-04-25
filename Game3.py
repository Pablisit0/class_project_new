import pygame
import random
import time
from pygame import Surface, image, transform
from Button_file import BeautifulButton
from EndScreen import EndScreen


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
        self.exit_callback = exit_callback
        self.quit_callback = quit_callback
        self.square_image = image.load("bobr_game.png")
        self.reset_game()

    def reset_game(self):
        self.grid_size = 3
        self.cell_size = 600 // self.grid_size
        self.squares = []
        self.score = 0
        self.misses = 0
        self.last_spawn_time = time.time()
        self.initial_spawn_interval = 0.5
        self.spawn_interval = self.initial_spawn_interval
        self.game_active = True
        self.restart_requested = False
        self.last_speed_increase_score = 0

    def update_difficulty(self):
        if self.score >= self.last_speed_increase_score + 25:
            self.last_speed_increase_score = self.score
            self.spawn_interval = max(0.1, self.spawn_interval - 0.05)

    def draw_grid(self):
        for x in range(1, self.grid_size):
            pygame.draw.line(self.screen, (200, 200, 200),
                             (x * self.cell_size, 0),
                             (x * self.cell_size, 600), 2)
            pygame.draw.line(self.screen, (200, 200, 200),
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
                self.squares.append(Square(x, y, 70, 90, self.cell_size, self.square_image))
            else:
                self.show_end_screen()

    def handle_click(self, mouse_x, mouse_y):
        clicked_on_square = False
        for square in self.squares[:]:
            if square.rect.collidepoint(mouse_x, mouse_y):
                self.squares.remove(square)
                self.score += 1
                self.update_difficulty()
                clicked_on_square = True

        if not clicked_on_square and 0 <= mouse_x < 600 and 0 <= mouse_y < 600:
            self.misses += 1

    def draw_stats(self):
        font = pygame.font.SysFont('Arial', 24)

        # Счёт в левом верхнем углу
        score_text = font.render(f"Score: {self.score}", True, (50, 50, 50))
        self.screen.blit(score_text, (20, 20))

        # Промахи в правом верхнем углу
        misses_text = font.render(f"Misses: {self.misses}", True, (50, 50, 50))
        misses_rect = misses_text.get_rect(topright=(580, 20))
        self.screen.blit(misses_text, misses_rect)

    def show_end_screen(self):
        end_screen = EndScreen(
            screen=self.screen,
            width=600,
            height=600,
            message="Game over",
            score=f"{self.score} | Misses: {self.misses}"
        )
        end_screen.run(
            restart_callback=self.request_restart,
            quit_callback=self.exit_callback
        )
        self.game_active = False

    def request_restart(self):
        self.restart_requested = True

    def run(self):
        while True:
            self.reset_game()
            running = True

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit_callback()
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.exit_callback()
                            return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.handle_click(*pygame.mouse.get_pos())

                if self.game_active:
                    self.spawn_square()

                    self.screen.fill((240, 240, 240))
                    self.draw_grid()
                    for square in self.squares:
                        square.draw(self.screen)
                    self.draw_stats()

                    if len(self.squares) >= 9:
                        self.show_end_screen()
                        running = False

                pygame.display.update()
                pygame.time.Clock().tick(60)

                if self.restart_requested:
                    running = False
                    break

            if not self.restart_requested:
                break