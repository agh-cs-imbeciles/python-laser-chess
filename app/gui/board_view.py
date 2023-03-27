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


class MetaAB(type(obs.PositionObserver), type(Screen)):
    pass


class Board(obs.PositionObserver, Screen, metaclass=MetaAB):
    def __init__(self, **kwargs):
        super().__init__()
        self._game = g.Game()
        self._grid = self.ids.board
        self._positions = empty(shape=(8, 8), dtype=RelativeLayout)
        self._dots = empty(shape=27, dtype=Image)
        self._representations = empty(shape=(8, 8), dtype=gui.PieceRepresentation)
        self._current_dots = []
        self._init_board()
        self._selected = None
        self._board = self._game.board

    def _init_board(self):
        board = self._game.board
        for i in range(8):
            for j in range(8):
                vector = Vector2d(j, 7 - i)

                field_layout = RelativeLayout()
                button = Button()
                button.vector = vector
                button.bind(on_press=self.on_tile_click)
                button.background_normal = ""
                field_layout.add_widget(button)
                piece = board.get_piece(vector)

                if piece is not None:
                    piece.add_observer(self)
                    piece_rep = gui.PieceRepresentation(piece.model, piece.player_id)
                    self._representations[vector.x][vector.y] = piece_rep
                    img = piece_rep.get_representation()
                    field_layout.add_widget(img)
                self._positions[vector.y][vector.x] = field_layout
                if (i + j) % 2 == 0:
                    button.background_color = rgba_int_to_float((150, 50, 50, 255))
                else:
                    button.background_color = rgba_int_to_float((54, 54, 54, 255))

                self._grid.add_widget(self._positions[vector.y][vector.x])

        for i in range(len(self._dots)):
            self._dots[i] = Image(source="assets/dot.png")
        # self.on_move(Vector2d(0, 0), Vector2d(5, 3))
        # self.on_show_possible_movements([Vector2d(0, 1), Vector2d(3, 2)])

    def on_tile_click(self, instance: Button):
        for d in self._current_dots:
            d.parent.remove_widget(d)
        self._current_dots.clear()

        if self._selected is None:
            self._selected = self._board.get_piece_movement(instance.vector)
            self.on_show_possible_movements(self._selected.get_legal_moves())
            return

        self._selected._piece.move(instance.vector)

    def on_show_possible_movements(self, movements: list[Vector2d]):
        i = 0
        for m in movements:
            self._positions[m.y][m.x].add_widget(self._dots[i])
            self._current_dots.append(self._dots[i])
            i += 1

    def on_position_change(self, origin: Vector2d, destination: Vector2d) -> None:
        from_rel = self._positions[origin.y][origin.x]
        piece_representation = from_rel.children[0]
        from_rel.remove_widget(piece_representation)
        to_rel = self._positions[destination.y][destination.x]
        to_rel.add_widget(piece_representation)

    def update_representation(self, from_piece: pcs.Piece, to_piece: pcs.Piece):
        pass
