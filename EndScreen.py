import pygame
from Button_file import BeautifulButton

class EndScreen:
    def __init__(self, screen, width, height, message, score=None):
        self.screen = screen
        self.width = width
        self.height = height
        self.message = message
        self.score = score

        button_width = 200
        button_height = 50
        self.restart_button = BeautifulButton("Restart", (self.width - button_width) // 2, 350, button_width, button_height)
        self.quit_button = BeautifulButton("Quit", (self.width - button_width) // 2, 420, button_width, button_height)

    def run(self, restart_callback, quit_callback):
        font = pygame.font.Font(None, 72)
        running = True
        while running:
            self.screen.fill((255, 255, 255))

            title_text = font.render(self.message, True, (255, 0, 0))
            title_rect = title_text.get_rect(center=(self.width // 2, self.height // 3))
            self.screen.blit(title_text, title_rect)

            if self.score is not None:
                score_font = pygame.font.Font(None, 48)
                score_text = score_font.render(f"Score: {self.score}", True, (0, 0, 0))
                score_rect = score_text.get_rect(center=(self.width // 2, self.height // 3 + 80))
                self.screen.blit(score_text, score_rect)

            mouse_pos = pygame.mouse.get_pos()
            self.restart_button.draw(self.screen)
            self.quit_button.draw(self.screen)

            self.restart_button.check_hover(mouse_pos)
            self.quit_button.check_hover(mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit_callback()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.restart_button.check_click(mouse_pos):
                        restart_callback()
                        return
                    if self.quit_button.check_click(mouse_pos):
                        quit_callback()
                        return

            pygame.display.update()
