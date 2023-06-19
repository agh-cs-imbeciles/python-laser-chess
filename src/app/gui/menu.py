from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput
from app.gui.board_view import Board
from app.config.settings import SettingsGameplay
from app.gui.join_game_popup import JoinGamePopup


class Menu(Screen):
    def __init__(self, **kwargs):
        super().__init__()
        self._popup = JoinGamePopup()

    def create_new_board(self,button):
        Builder.load_file("app/templates/board.kv")
        self.manager.add_widget(Board(name="board"))
        self.manager.current="board"

    def join_game_popup(self, button):

        self._popup.bind(create_clicked=self.create_game)
        self._popup.bind(join_clicked=self.join_game)
        self._popup.open()

    def create_game(self,instance,value):
        print(self._popup.host_code)
        pass

    def join_game(self,instance,value):
        print(self._popup.join_code)
        pass

    def _update_width(self):
        self.ids.menu_box.height = self.ids.menu_box.width / 2

    def set_game_settings(self, gameplay: SettingsGameplay):
        print("Hi")
