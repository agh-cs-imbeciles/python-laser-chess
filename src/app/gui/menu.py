from __future__ import annotations
import asyncio

from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from app.gui import BoardView
from app.game import PreGameHelper
from app.client import Receiver
from app.config.settings import SettingsGameplay


class MenuView(Screen):
    def __init__(self, **kwargs):
        super().__init__()
        self.code = "2137"
        self.__game_id_label: TextInput = TextInput()
        self.__join_input: TextInput = TextInput()

    def create_new_board(
            self, online: bool = False,
            game_id: str | None = None,
            player_id: str | None = None):
        Builder.load_file("app/templates/board.kv")
        self.manager.add_widget(BoardView(name="board", online=online, game_id=game_id, player_id=player_id))
        self.manager.current = "board"

    def __code(self, instance, value):
        self.code = value

    def pregame_popup(self, button):
        popup = Popup(size_hint=(1, 0.5))
        title = "Play online game"
        content = BoxLayout(orientation="vertical")

        l1 = Label(text="Create the new game")
        l2 = Label(text="Join to the existing game")
        b1 = Button(text="Create the game")
        b1.bind(on_press=self.create_online_game)
        game_id_label = self.__game_id_label
        game_id_label.readonly = True
        game_id_label.background_color = (0, 0, 0, 0)
        game_id_label.foreground_color = (.9, .9, .9, 1)
        game_id_label.cursor_color = (0, 0, 0, 0)

        b2 = Button(text="Join the game")
        b2.bind(on_press=self.join_online_game)
        text_input = self.__join_input
        text_input.hint_text = "Game ID"

        content.add_widget(l1)
        content.add_widget(b1)
        content.add_widget(game_id_label)
        content.add_widget(l2)
        content.add_widget(text_input)
        content.add_widget(b2)

        popup.title = title
        popup.size_hint_min = (200, 200)
        popup.size_hint_max = (300, 300)
        popup.content = content
        popup.open()

    def __set_game_id(self, game_id: str):
        print(game_id)
        self.__game_id_label.text = game_id

    def create_online_game(self, instance):
        async def create_online_game_async():
            game_id, player_id = await PreGameHelper.create_game()
            self.__set_game_id(game_id)
            # await PreGameHelper.wait_for_other_player()
            # self.create_new_board(True, game_id, player_id)

        asyncio.run(create_online_game_async())

    def join_online_game(self, instance):
        async def join_online_game_async(game_id: str):
            try:
                player_id = await PreGameHelper.join_game(game_id)
                print(player_id)
            except RuntimeError:
                pass

        game_id: str = self.__join_input.text
        asyncio.run(join_online_game_async(game_id))

    def _update_width(self):
        self.ids.menu_box.height = self.ids.menu_box.width / 2
