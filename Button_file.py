import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)

class Button:
    def __init__(self, text, x, y, width, height, action=None):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.action = action
        self.color = (30, 144, 255)
        self.hover_color = (70, 130, 180)
        self.click_color = (0, 0, 205)
        self.original_color = (30, 144, 255)

    def draw(self, screen):
        # Рисуем кнопку с красивыми эффектами
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:  # Клик мыши
                pygame.draw.rect(screen, self.click_color, self.rect, border_radius=15)
            else:  # Наведение мыши
                pygame.draw.rect(screen, self.hover_color, self.rect, border_radius=15)
        else:  # Обычное состояние
            pygame.draw.rect(screen, self.color, self.rect, border_radius=15)

        # Тень для кнопки
        shadow_rect = self.rect.move(5, 5)
        pygame.draw.rect(screen, DARK_GRAY, shadow_rect, border_radius=15)

        # Текст на кнопке
        font = pygame.font.SysFont('Arial', 40)
        text_surface = font.render(self.text, True, WHITE)
        screen.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                   self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def is_hovered(self, pos):
        return self.rect.collidepoint(pos)

    def click(self):
        if self.action:
            self.action()
