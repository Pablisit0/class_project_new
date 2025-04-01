import pygame
from pygame import *
import random
import time
from Blocks_physics import Platform
from PlayerMovement import Player
from Button_file import BeautifulButton

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

        self.screen = pygame.display.set_mode(self.DISPLAY)
        pygame.display.set_caption("Game1")
        self.bg = Surface((self.WIN_WIDTH, self.WIN_HEIGHT))
        self.bg.fill(Color(self.BACKGROUND_COLOR))

        self.hero = Player(55, 55)
        self.left = self.right = False
        self.up = False

        self.entities.add(self.hero)

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
        self.spawn_interval = 1

        self.start_time = time.time()
        self.timer_font = pygame.font.Font(None, 36)

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
                if self.score == 4:
                    self.you_won()
                    return False

        return True

    def update(self):
        for o in self.objects:
            o.update()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.hero.update(self.left, self.right, self.up, self.platforms)
        self.entities.draw(self.screen)


        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Coins: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 5))


        elapsed_time = int(time.time() - self.start_time)
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
        self.show_end_screen("You Won!")

    def show_end_screen(self, message):
        # Белый фон
        self.screen.fill((255, 255, 255))


        font = pygame.font.Font(None, 72)  # Крупный шрифт
        text = font.render(message, True, (255, 0, 0))  # Красный цвет
        text_rect = text.get_rect(center=(self.WIN_WIDTH // 2, self.WIN_HEIGHT // 3))
        self.screen.blit(text, text_rect)


        restart_button = BeautifulButton("Restart", 300, 350, 200, 50)
        quit_button = BeautifulButton("Quit", 300, 420, 200, 50)

        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()


            restart_button.draw(self.screen)
            quit_button.draw(self.screen)


            restart_button.check_hover(mouse_pos)
            quit_button.check_hover(mouse_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button.check_click(mouse_pos):
                        self.__init__(self.exit, self.quit)
                        self.run()
                        return
                    if quit_button.check_click(mouse_pos):
                        self.exit()
                        return

            pygame.display.update()

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