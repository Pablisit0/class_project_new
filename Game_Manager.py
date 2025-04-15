import pygame
import sys
from MainMenu import MainMenu
from MainMenu import LevelSelectMenu
from Game1 import Game_1
from Game2 import Game_2
from Game3 import Game_3


class GameManager:
    def __init__(self):
        pygame.init()
        self.STATE_MENU = "menu"
        self.STATE_GAME_1 = "game_1"
        self.STATE_GAME_2 = "game_2"
        self.STATE_GAME_3 = "game_3"
        self.STATE_LEVEL_SELECT = "level_select"  # Новое состояние
        self.current_state = self.STATE_MENU
        self.main_menu = MainMenu(self.start_game, self.quit)
        self.level_select_menu = None  # Будет инициализировано при необходимости
        self.active_game = None

    def start_game(self, game_name):
        if game_name == "game_1":
            # Вместо непосредственного запуска игры, показываем меню выбора уровня
            self.level_select_menu = LevelSelectMenu(self.start_selected_level, self.exit_to_menu)
            self.current_state = self.STATE_LEVEL_SELECT
        elif game_name == "game_2":
            self.active_game = Game_2(self.exit_to_menu, self.quit)
            self.current_state = self.STATE_GAME_2
        elif game_name == "game_3":
            self.active_game = Game_3(self.exit_to_menu, self.quit)
            self.current_state = self.STATE_GAME_3

    def start_selected_level(self, level_num):
        # Запускаем Game1 с выбранным уровнем
        self.active_game = Game_1(self.exit_to_menu, self.quit, level_num)
        self.current_state = self.STATE_GAME_1

    def exit_to_menu(self):
        if self.active_game:
            self.active_game = None
        if self.level_select_menu:
            self.level_select_menu = None
        self.current_state = self.STATE_MENU
        self.main_menu = MainMenu(self.start_game, self.quit)

    def quit(self):
        pygame.quit()
        sys.exit()

    def run(self):
        while True:
            if self.current_state == self.STATE_MENU:
                self.main_menu.run()
            elif self.current_state == self.STATE_LEVEL_SELECT:
                self.level_select_menu.run()
            else:
                if self.active_game:
                    self.active_game.run()


if __name__ == "__main__":
    game_manager = GameManager()
    game_manager.run()