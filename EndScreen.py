import pygame

class EndScreen:
    def __init__(self, screen, exit_callback, restart_callback):
        self.screen = screen
        self.exit_callback = exit_callback
        self.restart_callback = restart_callback
        self.font = pygame.font.Font(None, 72)
        self.button_font = pygame.font.Font(None, 36)
        self.title_text = self.font.render("Игра окончена!", True, (255, 0, 0))
        self.restart_button = pygame.Rect(200, 300, 200, 50)
        self.quit_button = pygame.Rect(200, 370, 200, 50)

    def draw(self):
        self.screen.fill((0, 0, 0))


        title_rect = self.title_text.get_rect(center=(self.screen.get_width() // 2, 150))
        self.screen.blit(self.title_text, title_rect)


        pygame.draw.rect(self.screen, (0, 255, 0), self.restart_button)
        restart_text = self.button_font.render("Заново", True, (0, 0, 0))
        restart_text_rect = restart_text.get_rect(center=self.restart_button.center)
        self.screen.blit(restart_text, restart_text_rect)


        pygame.draw.rect(self.screen, (255, 0, 0), self.quit_button)
        quit_text = self.button_font.render("Выход", True, (0, 0, 0))
        quit_text_rect = quit_text.get_rect(center=self.quit_button.center)
        self.screen.blit(quit_text, quit_text_rect)

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_callback()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if self.restart_button.collidepoint(mouse_pos):
                    self.restart_callback()
                elif self.quit_button.collidepoint(mouse_pos):
                    self.exit_callback()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.exit_callback()