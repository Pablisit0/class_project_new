import pygame
import random
from EndScreen import EndScreen

WIN_WIDTH = 400
WIN_HEIGHT = 600
PIPE_GAP = 150
PIPE_FREQUENCY = 1500
GROUND_HEIGHT = 100
BIRD_WIDTH = 40
BIRD_HEIGHT = 30
PIPE_WIDTH = 70


class Bird:
    def __init__(self):
        self.x = 100
        self.y = WIN_HEIGHT // 4
        self.velocity = 0
        self.gravity = 0.5
        self.jump_strength = -10
        self.image = pygame.image.load("bobr_game.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (BIRD_WIDTH, BIRD_HEIGHT))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        self.rect.y = self.y

    def jump(self):
        self.velocity = self.jump_strength

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Pipe:
    def __init__(self):
        self.x = WIN_WIDTH
        self.height = random.randint(100, WIN_HEIGHT - GROUND_HEIGHT - PIPE_GAP - 100)
        self.pipe_top_img = pygame.image.load("pipe_bottom.png").convert_alpha()
        self.pipe_bottom_img = pygame.image.load("pipe.png").convert_alpha()
        self.pipe_top_img = pygame.transform.scale(self.pipe_top_img, (PIPE_WIDTH, self.height))
        self.pipe_bottom_img = pygame.transform.scale(self.pipe_bottom_img,
                                                      (PIPE_WIDTH, WIN_HEIGHT - self.height - PIPE_GAP))
        self.top_rect = self.pipe_top_img.get_rect(topleft=(self.x, 0))
        self.bottom_rect = self.pipe_bottom_img.get_rect(topleft=(self.x, self.height + PIPE_GAP))
        self.passed = False
        self.speed = 3

    def update(self):
        self.x -= self.speed
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self, screen):
        screen.blit(self.pipe_top_img, self.top_rect)
        screen.blit(self.pipe_bottom_img, self.bottom_rect)


class Game_2:
    def __init__(self, exit_callback, quit_callback):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        pygame.display.set_caption("Game 2")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 30)
        self.exit_callback = exit_callback
        self.quit_callback = quit_callback
        self.restart_requested = False
        self.reset_game()

    def reset_game(self):
        self.bird = Bird()
        self.pipes = []
        self.score = 0
        self.last_pipe = pygame.time.get_ticks()
        self.game_active = True
        self.game_started = False
        self.restart_requested = False

    def check_collisions(self):
        if self.bird.rect.bottom >= WIN_HEIGHT - GROUND_HEIGHT:
            return True
        if self.bird.rect.top <= 0:
            return True
        for pipe in self.pipes:
            if (self.bird.rect.colliderect(pipe.top_rect) or
                    self.bird.rect.colliderect(pipe.bottom_rect)):
                return True
        return False

    def show_end_screen(self):
        end_screen = EndScreen(
            screen=self.screen,
            width=WIN_WIDTH,
            height=WIN_HEIGHT,
            message="Game Over",
            score=self.score
        )
        end_screen.run(
            restart_callback=self.request_restart,
            quit_callback=self.exit_callback
        )

    def request_restart(self):
        self.restart_requested = True

    def run(self):
        while True:
            self.reset_game()
            running = True

            while running:
                current_time = pygame.time.get_ticks()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.quit_callback()
                        return
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.bird.jump()
                            self.game_started = True
                        if event.key == pygame.K_ESCAPE:
                            self.exit_callback()
                            return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.bird.jump()
                        self.game_started = True

                if self.game_active:
                    if current_time - self.last_pipe > PIPE_FREQUENCY and self.game_started:
                        self.pipes.append(Pipe())
                        self.last_pipe = current_time

                    self.bird.update()
                    for pipe in self.pipes:
                        pipe.update()

                    self.pipes = [pipe for pipe in self.pipes if pipe.x > -PIPE_WIDTH]

                    if self.check_collisions():
                        self.show_end_screen()
                        running = False

                    for pipe in self.pipes:
                        if pipe.x + PIPE_WIDTH < self.bird.x and not pipe.passed:
                            pipe.passed = True
                            self.score += 1

                self.screen.fill((135, 206, 235))
                for pipe in self.pipes:
                    pipe.draw(self.screen)
                self.bird.draw(self.screen)
                pygame.draw.rect(self.screen, (139, 69, 19), (0, WIN_HEIGHT - GROUND_HEIGHT, WIN_WIDTH, GROUND_HEIGHT))
                score_text = self.font.render(str(self.score), True, (255, 255, 255))
                self.screen.blit(score_text, (WIN_WIDTH // 2 - 10, 50))
                pygame.display.update()
                self.clock.tick(60)

                if self.restart_requested:
                    running = False
                    break

            if not self.restart_requested:
                break