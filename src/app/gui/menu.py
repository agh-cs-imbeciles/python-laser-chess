from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from app.config.settings import SettingsGameplay
from app.gui.board_view import Board


class Menu(Screen):
    def __init__(self, **kwargs):
        super().__init__()

    def create_new_board(self,button):
        Builder.load_file("app/templates/board.kv")
        #init w Board można zmodyfikować by przyjmował dodatkowe wartości
        self.manager.add_widget(Board(name="board"))
        self.manager.current="board"

    def _update_width(self):
        self.ids.menu_box.height = self.ids.menu_box.width / 2

    def set_game_settings(self, gameplay: SettingsGameplay):
        print("Hi")
