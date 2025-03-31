import pygame
import random
import time
from pygame import Surface, image, transform
from Button_file import BeautifulButton


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
        self.last_spawn_time = time.time()
        self.spawn_interval = 0.5
        self.game_active = True
        self.in_end_screen = False

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
                self.game_over = True
                self.show_game_over_screen = True

    def handle_click(self, mouse_x, mouse_y):
        for square in self.squares[:]:
            if square.rect.collidepoint(mouse_x, mouse_y):
                self.squares.remove(square)
                self.score += 1

    def draw_score(self):
        font = pygame.font.SysFont('Arial', 36, bold=True)
        text = font.render(f"Счет: {self.score}", True, (50, 50, 50))
        self.screen.blit(text, (20, 20))

    def show_end_screen(self):
        self.in_end_screen = True


        overlay = Surface((600, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))


        font = pygame.font.SysFont('Arial', 72, bold=True)
        text = font.render("Игра окончена!", True, (255, 100, 100))
        text_rect = text.get_rect(center=(300, 150))


        score_text = font.render(f"Счет: {self.score}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(300, 250))


        restart_btn = BeautifulButton("Заново", 150, 350, 300, 60)
        menu_btn = BeautifulButton("Выход", 150, 450, 300, 60)

        while self.in_end_screen:
            mouse_pos = pygame.mouse.get_pos()


            self.screen.fill((240, 240, 240))
            self.draw_grid()
            for square in self.squares:
                square.draw(self.screen)


            self.screen.blit(overlay, (0, 0))
            self.screen.blit(text, text_rect)
            self.screen.blit(score_text, score_rect)
            restart_btn.draw(self.screen)
            menu_btn.draw(self.screen)


            restart_btn.check_hover(mouse_pos)
            menu_btn.check_hover(mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_callback()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_btn.check_click(mouse_pos):
                        self.reset_game()
                        self.in_end_screen = False
                        return

                    if menu_btn.check_click(mouse_pos):
                        self.in_end_screen = False
                        self.game_active = False
                        self.exit_callback()
                        return

            pygame.display.flip()
            pygame.time.Clock().tick(60)

    def run(self):
        self.game_active = True

        while self.game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_callback()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.game_active = False
                        self.exit_callback()

                if event.type == pygame.MOUSEBUTTONDOWN and not self.in_end_screen:
                    self.handle_click(*pygame.mouse.get_pos())


            if not self.in_end_screen:
                self.spawn_square()


                self.screen.fill((240, 240, 240))
                self.draw_grid()
                for square in self.squares:
                    square.draw(self.screen)
                self.draw_score()


                if len(self.squares) >= 9:  # Все клетки заполнены
                    self.in_end_screen = True
                    self.show_end_screen()

            pygame.display.update()
            pygame.time.Clock().tick(60)