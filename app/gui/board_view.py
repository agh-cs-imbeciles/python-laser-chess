from typing import Any, Optional, Tuple
from kivy.graphics import Rectangle, Color
from kivy.graphics.instructions import Callback
from kivy.properties import ColorProperty, NumericProperty
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.screenmanager import Screen
import gui
from utils import Vector2d, rgba_int_to_float
import game as g
import game.pieces as pcs
import game.observer as obs
from numpy import empty
from gui.piece_representation import PieceRepresentationLayout


class MetaAB(type(obs.PositionObserver), type(Screen)):
    pass


class Board(obs.PositionObserver, Screen, metaclass=MetaAB):
    def __init__(self, **kwargs):
        super().__init__()
        self._game = g.Game()
        self._grid = self.ids.board
        self._dots = empty(shape=27, dtype=Image)
        self._representations = empty(shape=(8, 8), dtype=PieceRepresentationLayout)
        self._current_dots = []
        self._init_board()
        self._selected = None
        self._selected_piece = None
        self._board = self._game.board

    def _init_board(self):
        board = self._game.board
        for i in range(8):
            for j in range(8):
                vector = Vector2d(j, 7 - i)

                button = Button()
                button.vector = vector
                button.bind(on_press=self.on_tile_click)
                button.background_normal = ""
                piece = board.get_piece(vector)
                if piece is not None:
                    piece.add_observer(self)
                if (i + j) % 2 == 0:
                    button.background_color = rgba_int_to_float((150, 50, 50, 255))
                else:
                    button.background_color = rgba_int_to_float((54, 54, 54, 255))
                piece_layout = PieceRepresentationLayout(piece, button)
                self._grid.add_widget(piece_layout)
                self._representations[vector.y][vector.x] = piece_layout
        for i in range(len(self._dots)):
            self._dots[i] = Image(source="assets/dot.png")

    def on_tile_click(self, instance: Button):
        for d in self._current_dots:
            d.parent.remove_widget(d)
        self._current_dots.clear()
        if self._selected is None:
            self._selected = self._board.get_piece_movement(instance.vector)
            self._selected_piece = self._board.get_piece(instance.vector)
            if self._selected is None or self._selected_piece.player_id != self._board.move_number:
                self._selected = None
                self._selected_piece = None
                return
            self.on_show_possible_movements(self._selected.get_legal_moves())
            return
        self._board.move_piece_if_possible(self._selected_piece, instance.vector)
        self._selected = None
        self._selected_piece = None

    def on_show_possible_movements(self, movements: list[Vector2d]):
        i = 0
        for m in movements:
            self._representations[m.y][m.x].add_widget(self._dots[i])
            self._current_dots.append(self._dots[i])
            i += 1

    def on_position_change(self, origin: Vector2d, destination: Vector2d) -> None:
        img = self._representations[origin.y][origin.x].remove_img()
        self._representations[destination.y][destination.x].add_img(img)
        # from_rel = self._positions[origin.y][origin.x]
        # piece_representation = from_rel.children[0]
        # from_rel.remove_widget(piece_representation)
        # to_rel = self._positions[destination.y][destination.x]
        # to_rel.add_widget(piece_representation)

    def update_representation(self, from_piece: pcs.Piece, to_piece: pcs.Piece):
        pass
