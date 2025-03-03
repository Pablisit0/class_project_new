import pygame

class MainMenu:
    def __init__(self, start_game_callback, quit_callback):
        self.WIDTH, self.HEIGHT = 600, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Главное меню")
        self.start_game = start_game_callback
        self.quit = quit_callback

        # Логотип
        self.logo_image = pygame.image.load("logo_bobr_game.png")
        self.logo_image = pygame.transform.scale(self.logo_image, (400, 200))
        self.logo_rect = self.logo_image.get_rect(center=(self.WIDTH//2, 100))

        # Кнопки
        self.buttons = [
            {"text": "Игра 1", "rect": pygame.Rect(200, 250, 200, 50)},
            {"text": "Игра 2", "rect": pygame.Rect(200, 320, 200, 50)},
            {"text": "Игра 3", "rect": pygame.Rect(200, 390, 200, 50)},
            {"text": "Выход", "rect": pygame.Rect(200, 460, 200, 50)}
        ]

    def is_button_clicked(self, button_text, mouse_pos):
        for button in self.buttons:
            if button["text"] == button_text and button["rect"].collidepoint(mouse_pos):
                return True
        return False

    def draw(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.logo_image, self.logo_rect)
        for button in self.buttons:
            pygame.draw.rect(self.screen, (200, 200, 200), button["rect"])
            font = pygame.font.Font(None, 36)
            text = font.render(button["text"], True, (0, 0, 0))
            text_rect = text.get_rect(center=button["rect"].center)
            self.screen.blit(text, text_rect)
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.is_button_clicked("Игра 1", mouse_pos):
                        self.start_game("game_1")
                        running = False
                    elif self.is_button_clicked("Игра 2", mouse_pos):
                        self.start_game("game_2")
                        running = False
                    elif self.is_button_clicked("Игра 3", mouse_pos):
                        self.start_game("game_3")
                        running = False
                    elif self.is_button_clicked("Выход", mouse_pos):
                        self.quit()
