from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from game.piece import PieceModel
from game.piece.move import PieceMoveType
from utils import BoardVector2d
from app.gui.utils import rgba_int_to_float, ImageButtonLayout, Paths
import game as g
import game.observer as obs
from game.observer.game_end_obs import GameEndObserver
from numpy import empty
from app.gui.piece_representation import PieceRepresentationLayout
from app.gui.window_updater import WindowUpdater
from game.piece.piece import Piece
from app.game import GameApplication
from app.gui import Path
import itertools


class MetaAB(type(obs.PositionObserver), type(Screen)):
    pass


class Board(obs.PositionObserver, GameEndObserver, Screen, metaclass=MetaAB):
    def __init__(self, **kwargs):
        super().__init__()
        self._game = g.Game()
        self._game_app: GameApplication = GameApplication(self._game)
        self._grid = self.ids.board
        self._indicator_label: Label = self.ids.indicator_lab
        self._dots = empty(shape=27, dtype=Image)
        self._laser_ind = empty(shape=64, dtype=Image)
        self._representations = empty(shape=(8, 8), dtype=PieceRepresentationLayout)
        self._current_dots = []
        self._current_laser_ind = []
        self._selected = None
        self._selected_piece = None
        self._board = self._game.board
        self._possible_movements = []
        self._is_promotion = False
        self._window_updater = WindowUpdater(self.ids)
        self._promotion_representation: list[PieceRepresentationLayout]
        self._rotation_representation: list[ImageButtonLayout]
        self._reset_button = Button()
        self._reset_button.vector = BoardVector2d(-1, -1)
        self._init_board()
        self._elements_dict = dict()

        for id in self.ids:
            t = self.ids.get(id)
            self._elements_dict.update({id: t})
        self._window_updater = WindowUpdater(self._elements_dict)

    def _init_board(self):
        board = self._game.board

        # assigning observer to game
        self._game.add_observer(self)

        # creation of indicator dots
        for i in range(len(self._dots)):
            self._dots[i] = Image(source=f"{Path.IMG_PATH}/dot.png")

        # creation of laser dots
        for i in range(len(self._laser_ind)):
            self._laser_ind[i] = Image(source=f"{Path.IMG_PATH}/lasgun_dot.png")

        self._add_coordinates()

        self.update_indicator_label("Tura gracza " + str(self._board.move_number))
        for i in range(8):
            for j in range(8):
                vector = BoardVector2d(j, 7 - i)

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

        # creation of promotion tab
        self._promotion_representation = [
            PieceRepresentationLayout(None, Button(on_press=self.on_promotion_click), opacity=0) for _ in self._board
            .get_possible_promotions()
        ]

        for rep in self._promotion_representation:
            self.ids.promotion_tab.add_widget(rep)

        # creation of rotation tab

        self._rotation_representation = [
            ImageButtonLayout(Paths.LEFT.value, Button(on_press=self.on_rotation_click), opacity=0),
            ImageButtonLayout(Paths.RIGHT.value, Button(on_press=self.on_rotation_click), opacity=0)
        ]
        r = self._rotation_representation
        r[0].add_value_to_button(Paths.LEFT)
        r[1].add_value_to_button(Paths.RIGHT)

        for rep in self._rotation_representation:
            self.ids.rotation_tab.add_widget(rep)

    def _add_coordinates(self):
        boxes = [self.ids.top, self.ids.left, self.ids.bot, self.ids.right]
        for i in range(8):
            for j in range(4):
                label = Label()
                if j % 2 == 1:
                    label.text = str(8 - i)
                else:
                    label.text = chr(i + 97)
                label.bold = True
                boxes[j].add_widget(label)

    def _show_checks(self):
        check = Image(source=f"{Path.IMG_PATH}/this_fire.png")
        for king in self._board.kings:
            if self._board.is_king_under_check(king.player_id):
                vector = king.position
                self._representations[vector.y][vector.x].add_indicator(check)

    def get_to_promote(self):
        return self._promotion.get_promotion_piece()

    def on_promotion_click(self, instance: Button):
        new = self._board.promote(instance.value)
        new[0].add_observer(self)
        for rep in self._promotion_representation:
            rep.remove_img()
            rep.opacity = 0
        self._is_promotion = False
        self.on_position_change(None, None)

    def on_rotation_click(self, instance: Button):
        match instance.value:
            case Paths.LEFT:
                self._game.move_piece(self._selected_piece, None, False)
            case Paths.RIGHT:
                self._game.move_piece(self._selected_piece, None, True)
        for rep in self._rotation_representation:
            rep.opacity = 0
        self.on_tile_click(self._reset_button)
        self._possible_movements = []
        self._selected = None
        self._selected_piece = None

    def hide_rotation(self):
        for rep in self._rotation_representation:
            rep.opacity = 0

    def clear_laser_ind(self):
        for l in self._current_laser_ind:
            l.parent.remove_widget(l)
        self._current_laser_ind.clear()

    def on_tile_click(self, instance: Button):
        self.hide_rotation()
        if self._is_promotion:
            return

        # clear indicating dots

        for d in self._current_dots:
            d.parent.remove_widget(d)
        self._current_dots.clear()

        piece = self._board.get_piece(instance.vector)
        if piece is not None and piece.is_same_color(self._board.move_number):
            if piece.model == PieceModel.LASGUN:
                self._board.fire_lasgun_control(piece.player_id)
                self.on_show_laser_fields(self._board.get_all_laser_fields())
                return
            self._selected_piece = self._board.get_piece(instance.vector)
            self._selected = self._board.get_piece_movement(instance.vector)
            self._possible_movements = list(itertools.chain.from_iterable(self._selected.get_legal_moves()))
            self.on_show_possible_movements(self._possible_movements)
            if piece.model == PieceModel.MIRROR and not self._board.is_king_under_check(piece.player_id):
                self.show_rotation_menu()
            return
        #
        # Move piece
        #
        if self._selected is not None and instance.vector in self._possible_movements:
            self.update_indicator_label("Tura gracza " + str(self._board.move_number))
            self._game.move_piece(self._selected_piece, instance.vector)
            self._game_app.on_move()
            self.show_promotion_menu(self._board.get_to_promote())
            self._possible_movements = []
            self._selected = None
            self._selected_piece = None

    def on_show_possible_movements(self, fields: list[BoardVector2d]):
        i = 0
        for m in fields:
            self._representations[m.y][m.x].add_widget(self._dots[i])
            self._current_dots.append(self._dots[i])
            i += 1

    def on_show_laser_fields(self, movements: list[BoardVector2d]):
        self.clear_laser_ind()
        i = 0
        for m in movements:
            self._representations[m.y][m.x].add_widget(self._laser_ind[i])
            self._current_laser_ind.append(self._laser_ind[i])
            i += 1

    # override
    def on_position_change(self, origin: BoardVector2d, destination: BoardVector2d) -> None:
        for i in range(len(self._representations)):
            for j in range(len(self._representations[i])):
                self._representations[i][j].remove_indicator()
                self._representations[i][j].remove_img()
                self._representations[i][j].new_image_piece(self._board.get_piece(BoardVector2d(j, i)))
        self._show_checks()
        self.clear_laser_ind()
        self.on_show_laser_fields(self._board.get_all_laser_fields())

    # override
    def on_end(self, winner: int, type: PieceMoveType) -> None:
        self.update_indicator_label("Szach mat. Wygrywa " + str(winner))

    def update_indicator_label(self, text: str):
        self._indicator_label.text = text
        pass

    def show_rotation_menu(self):
        for rep in self._rotation_representation:
            rep.opacity = 1
        pass

    def show_promotion_menu(self, piece: Piece):
        types = self._board.get_possible_promotions()
        if piece is None:
            return
        self._is_promotion = True

        for rep, tp in zip(self._promotion_representation, types):
            rep.add_value_to_button(tp)
            rep.opacity = 1
            rep.new_image(tp, piece.player_id)
