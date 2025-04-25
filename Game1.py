import pygame
from pygame import *
import random
import time
from Blocks_physics import Platform
from PlayerMovement import Player
from Button_file import BeautifulButton
from EndScreen import EndScreen


class Game_1:
    def __init__(self, exit_callback, quit_callback, start_level=0):
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
        self.current_level = start_level

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

        self.levels = [
            [
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
            ],
            [
                "-------------------------",
                "-                       -",
                "-                       -",
                "-         *             -",
                "-       ---             -",
                "-                       -",
                "---                  ----",
                "-                       -",
                "-       *               -",
                "-      ---          *   -",
                "-                  ---  -",
                "-                       -",
                "-                       -",
                "-              *        -",
                "-    -------------      -",
                "-                       -",
                "-                      *-",
                "-                     ---",
                "-                       -",
                "-------------------------"
            ],
            [
                "-------------------------",
                "-                       -",
                "-                       -",
                "-                *      -",
                "-       *               -",
                "-      ---              -",
                "-                       -",
                "-   *        ---        -",
                "-           --          -",
                "-         *             -",
                "-      ---              -",
                "-                       -",
                "-  *      ---     *     -",
                "-       ---             -",
                "-                       -",
                "-   ---           ---   -",
                "-                       -",
                "-                       -",
                "-                       -",
                "-------------------------"
            ],
            [
                "-------------------------",
                "-                       -",
                "-                       -",
                "-                       -",
                "-                       -",
                "-                       -",
                "-                       -",
                "- *                     -",
                "---                     -",
                "-                     * -",
                "-                     ---",
                "-                       -",
                "- *     -----           -",
                "---                     -",
                "-                       -",
                "-          -----        -",
                "- *                     -",
                "---                     -",
                "-                       -",
                "-------------------------"
            ]
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
        for platform in self.platforms:
            platform.kill()
        for coin in self.coins:
            coin.kill()

        self.platforms = []
        self.coins = []

        x = y = 0
        for row in self.levels[self.current_level]:
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
                if len(self.coins) == 0:
                    self.next_level()
                    return False

        return True

    def next_level(self):
        self.current_level += 1
        if self.current_level >= len(self.levels):
            self.you_won()
        else:
            for meteor in self.objects[:]:
                meteor.kill()
                self.objects.remove(meteor)

            self.hero.rect.x = 55
            self.hero.rect.y = 55
            self.load_level()

    def update(self):
        for obj in self.objects:
            obj.update()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.hero.update(self.left, self.right, self.up, self.platforms)
        self.entities.draw(self.screen)

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Coins: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 5))

        level_text = font.render(f"Level: {self.current_level + 1}/{len(self.levels)}", True, (255, 255, 255))
        self.screen.blit(level_text, (10, 40))

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
                if e.key == K_ESCAPE:
                    self.exit()
                    return False
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
        end_screen = EndScreen(
            screen=self.screen,
            width=self.WIN_WIDTH,
            height=self.WIN_HEIGHT,
            message=message,
            score=self.score
        )
        end_screen.run(
            restart_callback=lambda: self.restart_game(),
            quit_callback=self.exit
        )

    def restart_game(self):
        self.__init__(self.exit, self.quit)
        self.run()

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