from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from app.config.settings import SettingsGameplay


class Menu(Screen):
    def __init__(self, **kwargs):
        super().__init__()

    def _update_width(self):
        self.ids.menu_box.height = self.ids.menu_box.width / 2

    def set_game_settings(self, gameplay: SettingsGameplay):
        print("Hi")

