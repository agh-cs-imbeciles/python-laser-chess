from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from utils.background_label import BackgroundLabel
from game.piece.move import PieceMoveType
from utils import Vector2d, rgba_int_to_float
import game as g
import game.piece as pcs
import game.observer as obs
from game.observer.game_end_obs import GameEndObserver
from numpy import empty
from gui.piece_representation import PieceRepresentationLayout
from gui.window_updater import WindowUpdater
import itertools
class MetaAB(type(obs.PositionObserver), type(Screen)):
    pass


class Board(obs.PositionObserver, GameEndObserver, Screen, metaclass=MetaAB):
    def __init__(self, **kwargs):
        super().__init__()
        self._game = g.Game()
        self._grid = self.ids.board
        self._indicator_label:Label = self.ids.indicator_lab
        self._dots = empty(shape=27, dtype=Image)
        self._representations = empty(shape=(8, 8), dtype=PieceRepresentationLayout)
        self._current_dots = []
        self._selected = None
        self._selected_piece = None
        self._board = self._game.board
        self._possible_movements = []
        self._window_updater = WindowUpdater(self.ids)
        self._init_board()
        self._elements_dict = dict()
        for id in self.ids:
            t = self.ids.get(id)
            self._elements_dict.update({id:t})
        self._window_updater = WindowUpdater(self._elements_dict)

    def _init_board(self):
        board = self._game.board

        # assiging observer to game
        self._game.add_observer(self)

        # creation of indicator dots
        for i in range(len(self._dots)):
            self._dots[i] = Image(source="assets/dot.png")
        self._add_coordinates()


        self.update_indicator_label("Tura gracza "+str(self._board.move_number))
        for i in range(8):
            for j in range(8):
                vector = Vector2d(j, 7 - i)

                # preparation of every button on board

                button = Button()
                button.vector = vector
                button.bind(on_press=self.on_tile_click)
                button.background_normal = ""
                if (i + j) % 2 == 0:
                    button.background_color = rgba_int_to_float((150, 50, 50, 255))
                else:
                    button.background_color = rgba_int_to_float((54, 54, 54, 255))

                # assigning observer to piece

                piece = board.get_piece(vector)
                if piece is not None:
                    piece.add_observer(self)

                # adding piece and button to board

                piece_layout = PieceRepresentationLayout(piece, button)
                self._grid.add_widget(piece_layout)
                self._representations[vector.y][vector.x] = piece_layout


    def _add_coordinates(self):
        boxes = [self.ids.top, self.ids.left, self.ids.bot, self.ids.right]
        for i in range(8):
            for j in range(4):
                label = Label()
                if j % 2 == 1:
                    label.text = str(8-i)
                else:
                    label.text = chr(i+97)
                label.bold = True
                boxes[j].add_widget(label)

    def _show_checks(self):
        check = Image(source="assets/this_fire.png")
        for king in self._board.kings:
            if self._board.is_king_under_check(king.player_id):
                vector = king.position
                self._representations[vector.y][vector.x].add_indicator(check)

    def on_tile_click(self, instance: Button):
        # clear indicating dots

        for d in self._current_dots:
            d.parent.remove_widget(d)
        self._current_dots.clear()

        piece = self._board.get_piece(instance.vector)
        if self._selected is None:

            # select piece

            if piece is not None and piece.player_id == self._board.move_number:
                self._selected_piece = self._board.get_piece(instance.vector)
                self._selected = self._board.get_piece_movement(instance.vector)
                self._possible_movements = list(itertools.chain.from_iterable(self._selected.get_legal_moves()))
                self.on_show_possible_movements(self._possible_movements)
                return
        else:

            # select other piece

            if  piece is not None and piece.player_id == self._board.move_number:
                self._selected_piece = self._board.get_piece(instance.vector)
                self._selected = self._board.get_piece_movement(instance.vector)
                self._possible_movements = list(itertools.chain.from_iterable(self._selected.get_legal_moves()))
                self.on_show_possible_movements(self._possible_movements)

            # move piece

            elif instance.vector in self._possible_movements:
                self.update_indicator_label("Tura gracza " + str(self._board.move_number))
                self._game.move_piece(self._selected_piece, instance.vector)


            # reset

            self._possible_movements = []
            self._selected = None
            self._selected_piece = None

    def on_show_possible_movements(self, movements: list[Vector2d]):
        i = 0
        for m in movements:
            self._representations[m.y][m.x].add_widget(self._dots[i])
            self._current_dots.append(self._dots[i])
            i += 1

    # override
    def on_position_change(self, origin: Vector2d, destination: Vector2d) -> None:
        for i in range(len(self._representations)):
            for j in range(len(self._representations[i])):
                self._representations[i][j].remove_indicator()
                self._representations[i][j].remove_img()
                self._representations[i][j].new_image(self._board.get_piece(Vector2d(j, i)))
        self._show_checks()

    #override
    def on_end(self, winner: int, type: PieceMoveType) -> None:
        self.update_indicator_label("Szach mat. Wygrywa "+str(winner))

    def update_indicator_label(self, text: str):
        self._indicator_label.text = text
        pass