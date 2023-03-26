from kivy.graphics import Rectangle, Color
from kivy.graphics.instructions import Callback
from kivy.properties import ColorProperty, NumericProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from utils.kivy_utilities import rgba_int_to_float
from game.game import Game
from numpy import empty
from typing import Any, Optional, Tuple


class Board(Screen):
    def __init__(self, **kwargs):
        super().__init__()
        self._game = Game()
        self._grid = self.ids.board
        self._positions = empty(shape=(8, 8), dtype=object)
        self._init_board()

    def _init_board(self):
        for i in range(8):
            for j in range(8):
                field_layout = RelativeLayout()
                button = Button()
                button.indexes = (i, j)
                button.bind(on_press=self.on_click)
                button.background_normal = ""
                img_path = self._get_image_path(i, j)
                field_layout.add_widget(button)
                if img_path != None:
                    img = Image(source=img_path)
                    field_layout.add_widget(img)
                self._positions[i][j] = field_layout
                if (i + j) % 2 == 0:
                    button.background_color = rgba_int_to_float((150, 50, 50, 255))
                else:
                    button.background_color = rgba_int_to_float((54, 54, 54, 255))
                self._grid.add_widget(self._positions[i][j])

    def _get_image_path(self, i: int, j: int) -> Optional[str]:
        if i == 0:
            if j == 0 or j == 7:
                return "assets/b_rook.png"
            if j == 1 or j == 6:
                return "assets/b_knight.png"
            if j == 2 or j == 5:
                return "assets/b_bishop.png"
            if j == 3:
                return "assets/b_queen.png"
            if j == 4:
                return "assets/b_king.png"
        if i == 1:
            return "assets/b_pawn.png"
        if i == 7:
            if j == 0 or j == 7:
                return "assets/w_rook.png"
            if j == 1 or j == 6:
                return "assets/w_knight.png"
            if j == 2 or j == 5:
                return "assets/w_bishop.png"
            if j == 3:
                return "assets/w_queen.png"
            if j == 4:
                return "assets/w_king.png"
        if i == 6:
            return "assets/w_pawn.png"
        return None

    def on_click(self, instance: Button):
        print(instance.indexes)
