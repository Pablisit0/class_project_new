import pygame
from pygame import *
import random
import time
from Blocks_physics import Platform
from PlayerMovement import Player

class Game_1:
    def __init__(self, exit_to_menu_callback, quit_callback):
        self.exit_to_menu_callback = exit_to_menu_callback  # Функция для возврата в меню
        self.quit_callback = quit_callback  # Функция для выхода из игры
        self.WIN_WIDTH = 800  # Ширина создаваемого окна
        self.WIN_HEIGHT = 640  # Высота
        self.DISPLAY = (self.WIN_WIDTH, self.WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
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
        self.screen = pygame.display.set_mode(self.DISPLAY)  # Создаем окошко
        pygame.display.set_caption("Game1")  # Пишем в шапку
        self.bg = Surface((self.WIN_WIDTH, self.WIN_HEIGHT))  # Создание видимой поверхности
        self.bg.fill(Color(self.BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

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
            "-------------------------"]

        self.last_spawn_time = time.time()
        self.spawn_interval = 1  # Интервал спавна в секундах

    def spawn_object(self):
        spawn_point = random.choice(self.spawn_points)  # Выбор случайной точки спавна
        new_object = meteor('meteor.png', spawn_point.position)
        self.entities.add(new_object)  # Добавляем объект в группу спрайтов
        return new_object

    def load_level(self):
        x = y = 0  # начальные координаты
        for row in self.level:  # вся строка
            for col in row:  # каждый символ
                if col == "-":
                    pf = Platform(x, y)
                    self.entities.add(pf)
                    self.platforms.append(pf)
                elif col == "*":
                    coin = Coin(x, y)
                    self.entities.add(coin)
                    self.coins.append(coin)
                x += self.PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
            y += self.PLATFORM_HEIGHT  # то же самое и с высотой
            x = 0  # на каждой новой строчке начинаем с нуля

    def handle_collisions(self):
        for meteor in self.objects:
            if self.hero.rect.colliderect(meteor):
                print("Game Over")
                self.game_over()  # Показываем экран окончания игры
                return False

        for coin in self.coins[:]:  # Используем копию списка, чтобы изменять оригинал
            if self.hero.rect.colliderect(coin):
                self.coins.remove(coin)  # Удаляем монетку
                self.score += 1  # Увеличиваем счетчик монеток
                coin.kill()
                if self.score == 4:
                    print("You won!")
                    self.game_over()  # Показываем экран окончания игры
                    return False

        return True

    def update(self):
        # Обновление объектов
        for o in self.objects:
            o.update()

    def draw(self):
        self.screen.blit(self.bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать
        self.hero.update(self.left, self.right, self.up, self.platforms)  # передвижение
        self.entities.draw(self.screen)  # отображение всего
        font = pygame.font.Font(None, 36)
        text = font.render(f"Coins: {self.score}", True, (255, 255, 255))
        self.screen.blit(text, (10, 5))

    def handle_events(self):
        for e in pygame.event.get():  # Обрабатываем события
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
        font = pygame.font.Font(None, 72)
        text = font.render("Game Over", True, (255, 0, 0))
        restart_button = pygame.Rect(300, 300, 200, 50)
        quit_button = pygame.Rect(300, 400, 200, 50)

        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Заливаем экран черным цветом
            self.screen.blit(text, (250, 150))  # Показываем надпись "Game Over"

            pygame.draw.rect(self.screen, (0, 255, 0), restart_button)  # Кнопка "Повторить"
            pygame.draw.rect(self.screen, (255, 0, 0), quit_button)  # Кнопка "Выйти"

            restart_text = pygame.font.Font(None, 36).render("Restart", True, (0, 0, 0))
            quit_text = pygame.font.Font(None, 36).render("Quit", True, (0, 0, 0))
            self.screen.blit(restart_text, (restart_button.x + 60, restart_button.y + 10))
            self.screen.blit(quit_text, (quit_button.x + 70, quit_button.y + 10))

            pygame.display.update()  # Обновляем экран

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.quit_callback()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if restart_button.collidepoint(mouse_pos):
                        running = False
                        self.__init__(self.exit_to_menu_callback, self.quit_callback)  # Перезапуск игры
                        self.run()
                        return
                    if quit_button.collidepoint(mouse_pos):
                        running = False
                        self.exit_to_menu_callback()  # Возвращаемся в меню
                        return

    def run(self):
        self.load_level()  # Загружаем уровень
        running = True

        while running:  # Основной цикл программы
            pygame.time.Clock().tick(60)

            if not self.handle_events():
                break

            if time.time() - self.last_spawn_time > self.spawn_interval:
                self.objects.append(self.spawn_object())
                self.last_spawn_time = time.time()

            if not self.handle_collisions():
                running = False  # Остановка игры

            self.draw()
            self.update()

            pygame.display.update()  # обновление и вывод всех изменений на экран


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
        self.kill()  # Удаляем монету из игры


class SpawnPoint:
    def __init__(self, x, y):
        self.position = (x, y)


class meteor(pygame.sprite.Sprite):
    def __init__(self, image_path, position):
        super().__init__()
        self.image = image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.topleft = position
        self.speed_y = 5

    def update(self):
        # Обновление позиции: падение вниз
        self.rect.y += self.speed_y
        # Удаление объекта, если он ушел за границы экрана
        if self.rect.top > 640:
            self.kill()  # Убираем спрайт из игры
