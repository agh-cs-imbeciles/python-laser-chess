from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from app.gui import BoardView
from app.config.settings import SettingsGameplay


class MenuView(Screen):
    def __init__(self, **kwargs):
        super().__init__()
        self.code = "2137"

    def create_new_board(self, online: bool):
        Builder.load_file("app/templates/board.kv")
        self.manager.add_widget(BoardView(name="board", online=online))
        self.manager.current = "board"

    def __code(self, instance, value):
        self.code = value

    def join_game_popup(self,button):
        popup = Popup(size_hint=(0.6, 0.2))
        title = "Play online game"
        content = BoxLayout(orientation="vertical")
        l1 = Label(text="Create the new game")
        l2 = Label(text="Join to the existing game")
        b1 = Button(text="Create the game")
        b1.bind(on_press=self.create_game)
        b2 = Button(text="Join the game")
        b2.bind(on_press=self.join_game)
        text_input = TextInput(text="2137")
        text_input.bind(text=self.__code)
        content.add_widget(l1)
        content.add_widget(b1)
        content.add_widget(l2)
        content.add_widget(text_input)
        content.add_widget(b2)
        popup.title = title
        popup.size_hint_min = (200, 200)
        popup.size_hint_max = (300, 300)
        popup.content = content
        popup.open()

    def create_game(self, instance):
        pass

    def join_game(self, instance):
        print(self.code)
        pass

    def _update_width(self):
        self.ids.menu_box.height = self.ids.menu_box.width / 2

    def set_game_settings(self, gameplay: SettingsGameplay):
        print("Hi")
