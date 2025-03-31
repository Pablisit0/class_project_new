import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (150, 150, 150)

class BeautifulButton:
    def __init__(self, text, x, y, width, height):
        self.text = text
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (30, 144, 255)
        self.hover_color = (70, 130, 180)
        self.click_color = (0, 0, 205)
        self.font = pygame.font.Font(None, 36)
        self.is_hovered = False
        self.is_clicked = False

    def draw(self, screen):
        if self.is_clicked:
            color = self.click_color
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.color


        pygame.draw.rect(screen, color, self.rect, border_radius=15)


        text_surface = self.font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.is_clicked = True
            return True
        return False