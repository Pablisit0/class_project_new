import pygame
from Button_file import BeautifulButton

class LevelSelectMenu:
    def __init__(self, start_level_callback, back_callback):
        self.WIDTH, self.HEIGHT = 600, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Выбор уровня")
        self.start_level = start_level_callback
        self.back = back_callback

        # Заголовок
        self.font = pygame.font.Font(None, 48)
        self.title = self.font.render("Выберите уровень", True, (0, 0, 0))
        self.title_rect = self.title.get_rect(center=(self.WIDTH//2, 100))

        # Кнопки уровней
        self.buttons = [
            BeautifulButton("Уровень 1", 200, 200, 200, 50),
            BeautifulButton("Уровень 2", 200, 270, 200, 50),
            BeautifulButton("Уровень 3", 200, 340, 200, 50),
            BeautifulButton("Уровень 4", 200, 410, 200, 50),
            BeautifulButton("Назад", 200, 480, 200, 50)
        ]

    def draw(self):
        self.screen.fill((255, 255, 255))  # Белый фон
        self.screen.blit(self.title, self.title_rect)

        for button in self.buttons:
            button.draw(self.screen)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()

            for button in self.buttons:
                button.check_hover(mouse_pos)

            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.back()
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.check_click(mouse_pos):
                            if button.text == "Уровень 1":
                                self.start_level(0)
                                running = False
                            elif button.text == "Уровень 2":
                                self.start_level(1)
                                running = False
                            elif button.text == "Уровень 3":
                                self.start_level(2)
                                running = False
                            elif button.text == "Уровень 4":
                                self.start_level(3)
                                running = False
                            elif button.text == "Назад":
                                self.back()
                                running = False

class MainMenu:
    def __init__(self, start_game_callback, quit_callback):
        self.WIDTH, self.HEIGHT = 600, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Главное меню")
        self.start_game = start_game_callback
        self.quit = quit_callback


        self.logo_image = pygame.image.load("logo_bobr_game.png")
        self.logo_image = pygame.transform.scale(self.logo_image, (400, 200))
        self.logo_rect = self.logo_image.get_rect(center=(self.WIDTH//2, 100))


        self.buttons = [
            BeautifulButton("Game 1", 200, 250, 200, 50),
            BeautifulButton("Game 2", 200, 320, 200, 50),
            BeautifulButton("Game 3", 200, 390, 200, 50),
            BeautifulButton("Quit", 200, 460, 200, 50)
        ]

    def draw(self):
        self.screen.fill((255, 255, 255))  # Белый фон
        self.screen.blit(self.logo_image, self.logo_rect)  # Логотип


        for button in self.buttons:
            button.draw(self.screen)

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()


            for button in self.buttons:
                button.check_hover(mouse_pos)

            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for button in self.buttons:
                        if button.check_click(mouse_pos):
                            if button.text == "Game 1":
                                self.start_game("game_1")
                                running = False
                            elif button.text == "Game 2":
                                self.start_game("game_2")
                                running = False
                            elif button.text == "Game 3":
                                self.start_game("game_3")
                                running = False
                            elif button.text == "Quit":
                                self.quit()