from kivy.graphics import Rectangle, Color
from kivy.graphics.instructions import Callback
from kivy.properties import ColorProperty, NumericProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
from gui.gui_functions import _get_image_path
from utils.kivy_utilities import RGBA_to_tuple
from game.game import Game
from numpy import empty
from typing import Any, Optional, Tuple

from utils.vector2d import Vector2d


class Board(Screen):
    def __init__(self, **kwargs):
        super().__init__()
        self._game = Game()
        self._grid = self.ids.board
        self._positions = empty(shape=(8, 8), dtype=RelativeLayout)
        self._dots = empty(shape=27, dtype=Image)
        self._current_dots = []
        self._init_board()
    def _init_board(self):
        for i in range(8):
            for j in range(8):
                field_layout = RelativeLayout()
                button = Button()
                vector = Vector2d(j, 7-i)
                button.vector= vector
                button.bind(on_press=self.on_tile_click)
                button.background_normal = ""
                img_path = _get_image_path(vector)
                field_layout.add_widget(button)
                if img_path != None:
                    img = Image(source=img_path)
                    field_layout.add_widget(img)
                self._positions[vector.y][vector.x] = field_layout
                if (i + j) % 2 == 0:
                    button.background_color = RGBA_to_tuple((150, 50, 50, 255))
                else:
                    button.background_color = RGBA_to_tuple((54, 54, 54, 255))
                self._grid.add_widget(self._positions[vector.y][vector.x])
        for i in range(len(self._dots)):
            self._dots[i] = Image(source="assets/dot.png")
        self.on_move(Vector2d(0,0),Vector2d(5, 3))
        self.on_show_posible_movements([Vector2d(0,1),Vector2d(3,2)])

    def on_tile_click(self,instance: Button) -> Vector2d:
        for d in self._current_dots:
            d.parent.remove_widget(d)
        self._current_dots.clear()
        print(instance.vector)
        return Vector2d(instance.vector.x, instance.vector.y)

    def on_show_posible_movements(self, movements: list[Vector2d]):
        i = 0
        for m in movements:
            self._positions[m.y][m.x].add_widget(self._dots[i])
            self._current_dots.append(self._dots[i])
            i += 1

    def on_move(self, from_: Vector2d, to: Vector2d):
        from_rel = self._positions[from_.y][from_.x]
        piece_representation = from_rel.children[0]
        from_rel.remove_widget(piece_representation)
        to_rel = self._positions[to.y][to.x]
        to_rel.add_widget(piece_representation)




