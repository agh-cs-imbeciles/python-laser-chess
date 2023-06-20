from __future__ import annotations
from threading import Thread, main_thread
from functools import partial
import asyncio

from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from app.gui import BoardView
from app.game import PreGameHelper
from app.gui.join_game_popup import JoinGamePopup


class MenuView(Screen):
    def __init__(self, **kwargs):
        super().__init__()
        self.__game_id_label: TextInput | None = None
        self.__popup: JoinGamePopup = JoinGamePopup()

    def create_new_board(
            self, online: bool = False,
            game_id: str | None = None,
            player_id: str | None = None,
            *args):
        Builder.load_file("app/templates/board.kv")
        self.manager.add_widget(BoardView(name="board", online=online, game_id=game_id, player_id=player_id))
        self.manager.current = "board"

    def pregame_popup(self, button):
        self.__popup.bind(create_clicked=self.create_online_game)
        self.__popup.bind(join_clicked=self.join_online_game)
        self.__popup.open()

    def __set_game_id(self, game_id: str, *args):
        self.__popup.host_code = game_id

    def create_online_game(self, instance, value):
        async def create_online_game_async():
            game_id, player_id = await PreGameHelper.create_game()
            Clock.schedule_once(partial(self.__set_game_id, game_id))
            await PreGameHelper.wait_for_other_player(game_id)
            Clock.schedule_once(partial(self.create_new_board, True, game_id, player_id))

        thread: Thread = Thread(target=lambda: asyncio.run(create_online_game_async()))
        thread.start()

    def join_online_game(self, instance, value):
        async def join_online_game_async(game_id: str):
            try:
                player_id = await PreGameHelper.join_game(game_id)
                self.__popup.dismiss()
                self.create_new_board(True, game_id, player_id)
            except RuntimeError as error:
                print(error)

        game_id: str = self.__popup.join_code
        asyncio.run(join_online_game_async(game_id))
        self._popup.bind(create_clicked=self.create_game)
        self._popup.bind(join_clicked=self.join_game)
        self._popup.open()

    def _update_width(self):
        self.ids.menu_box.height = self.ids.menu_box.width / 2
