import pygame
from pygame import *
import random
import time
from Blocks_physics import Platform
from PlayerMovement import Player

class Game_1:
    def __init__(self, exit_callback, quit_callback):
        pygame.init()
        self.WIN_WIDTH = 800
        self.WIN_HEIGHT = 640
        self.DISPLAY = (self.WIN_WIDTH, self.WIN_HEIGHT)
        self.BACKGROUND_COLOR = "#000000"
        self.PLATFORM_WIDTH = 32
        self.PLATFORM_HEIGHT = 32
        self.PLATFORM_COLOR = "#FF6262"
        self.YELLOW = (255, 255, 0)
        self.BLACK = (0, 0, 0)

        self.entities = pygame.sprite.Group()
        self.meteorites = []
        self.score = 0
        self.coins = []
        self.platforms = []

        # Окно игры
        self.screen = pygame.display.set_mode(self.DISPLAY)
        pygame.display.set_caption("Game1")
        self.bg = Surface((self.WIN_WIDTH, self.WIN_HEIGHT))
        self.bg.fill(Color(self.BACKGROUND_COLOR))

        # Герой
        self.hero = Player(55, 55)
        self.left = self.right = False
        self.up = False

        self.entities.add(self.hero)

        # Точки спавна
        self.spawn_points = [
            SpawnPoint(100, -75),
            SpawnPoint(400, -75),
            SpawnPoint(700, -75)
        ]
        self.objects = []
        self.level = [
            "-------------------------",
            "-                       -",
            "-                       -",
            "-             *         -",
            "-            --         -",
            "-                       -",
            "--                      -",
            "-                     ---",
            "-                       -",
            "-       *               -",
            "-      ---        ---   -",
            "-                       -",
            "-           *           -",
            "-   -----------       ---",
            "-                       -",
            "-                -   *  -",
            "-                   --  -",
            "-                       -",
            "-                       -",
            "-------------------------"
        ]

        self.last_spawn_time = time.time()
        self.spawn_interval = 1  # Интервал спавна в секундах

        # Таймер
        self.start_time = time.time()  # Время начала уровня
        self.timer_font = pygame.font.Font(None, 36)  # Шрифт для таймера

        # Коллбеки
        self.exit = exit_callback
        self.quit = quit_callback

    def spawn_object(self):
        spawn_point = random.choice(self.spawn_points)
        new_object = meteor('meteor.png', spawn_point.position)
        self.entities.add(new_object)
        return new_object

    def load_level(self):
        x = y = 0
        for row in self.level:
            for col in row:
                if col == "-":
                    pf = Platform(x, y)
                    self.entities.add(pf)
                    self.platforms.append(pf)
                elif col == "*":
                    coin = Coin(x, y)
                    self.entities.add(coin)
                    self.coins.append(coin)
                x += self.PLATFORM_WIDTH
            y += self.PLATFORM_HEIGHT
            x = 0

    def handle_collisions(self):
        for meteor in self.objects:
            if self.hero.rect.colliderect(meteor):
                print("Game Over")
                self.game_over()
                return False

        for coin in self.coins[:]:
            if self.hero.rect.colliderect(coin):
                self.coins.remove(coin)
                self.score += 1
                coin.kill()
                if self.score == 4:  # Все монеты собраны
                    self.you_won()  # Показываем экран победы
                    return False

        return True

    def update(self):
        for o in self.objects:
            o.update()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.hero.update(self.left, self.right, self.up, self.platforms)
        self.entities.draw(self.screen)

        # Отрисовка счета
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Coins: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 5))

        # Отрисовка таймера
        elapsed_time = int(time.time() - self.start_time)  # Время в секундах
        timer_text = self.timer_font.render(f"Time: {elapsed_time}", True, (255, 255, 255))
        timer_rect = timer_text.get_rect(bottomright=(self.WIN_WIDTH - 10, self.WIN_HEIGHT - 10))
        self.screen.blit(timer_text, timer_rect)

    def handle_events(self):
        for e in pygame.event.get():
            if e.type == QUIT:
                return False
            if e.type == KEYDOWN:
                if e.key == K_LEFT:
                    self.left = True
                if e.key == K_RIGHT:
                    self.right = True
                if e.key == K_UP:
                    self.up = True
            if e.type == KEYUP:
                if e.key == K_RIGHT:
                    self.right = False
                if e.key == K_LEFT:
                    self.left = False
                if e.key == K_UP:
                    self.up = False
        return True

    def game_over(self):
        self.show_end_screen("Game Over")

    def you_won(self):
        self.show_end_screen("You won!")

    def show_end_screen(self, message):
        font = pygame.font.Font(None, 72)
        text = font.render(message, True, (255, 0, 0))
        restart_button = pygame.Rect(300, 300, 200, 50)
        quit_button = pygame.Rect(300, 400, 200, 50)

        running = True
        while running:
            self.screen.fill((0, 0, 0))
            self.screen.blit(text, (250, 150))

            pygame.draw.rect(self.screen, (0, 255, 0), restart_button)
            pygame.draw.rect(self.screen, (255, 0, 0), quit_button)

            restart_text = pygame.font.Font(None, 36).render("Restart", True, (0, 0, 0))
            quit_text = pygame.font.Font(None, 36).render("Quit", True, (0, 0, 0))
            self.screen.blit(restart_text, (restart_button.x + 60, restart_button.y + 10))
            self.screen.blit(quit_text, (quit_button.x + 70, quit_button.y + 10))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if restart_button.collidepoint(mouse_pos):
                        running = False
                        self.__init__(self.exit, self.quit)
                        self.run()
                        return
                    if quit_button.collidepoint(mouse_pos):
                        running = False
                        self.exit()
                        return

    def run(self):
        self.load_level()
        running = True

        while running:
            pygame.time.Clock().tick(60)

            if not self.handle_events():
                break

            if time.time() - self.last_spawn_time > self.spawn_interval:
                self.objects.append(self.spawn_object())
                self.last_spawn_time = time.time()

            if not self.handle_collisions():
                running = False

            self.draw()
            self.update()

            pygame.display.update()


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def handle_collision(self, player):
        player.coin_count += 1
        print(f"Монета собрана! Всего монет: {player.coin_count}")
        self.kill()


class SpawnPoint:
    def __init__(self, x, y):
        self.position = (x, y)


class meteor(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        super().__init__()
        self.image = image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.speed_y = 8

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > 640:
            self.kill()