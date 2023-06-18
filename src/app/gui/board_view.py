from random import randint
from typing import cast
import asyncio
import itertools

from kivy.graphics import Rectangle, Color
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen

from app.gui.laser_painter import LaserPainter
from app.gui.utils.common_font_label import CommonFontLabel
from game.piece import PieceModel
from game.piece.lasgun import Lasgun
from game.piece.move import PieceMoveType
from utils import BoardVector2d, Rotation
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


class MetaAB(type(obs.PositionObserver), type(Screen)):
    pass


class Board(obs.PositionObserver, GameEndObserver, Screen, metaclass=MetaAB):
    def __init__(self, **kwargs):
        super().__init__()
        self._game = g.Game()
        self._game_app: GameApplication = GameApplication(self._game, online=True)
        self._grid = self.ids.board
        self._indicator_label: Label = self.ids.indicator_lab
        self._dots = empty(shape=27, dtype=Image)
        self._representations = empty(shape=(8, 8), dtype=PieceRepresentationLayout)
        self._current_dots = []
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
        self._elements_dict = dict()
        self._notation_list = []
        self._laser_painer = LaserPainter(self, self._board)
        self._elements_dict["board_images"] = empty(shape=(8, 8), dtype=Image)
        for id in self.ids:
            t = self.ids.get(id)
            self._elements_dict.update({id: t})
        self._init_board()
        self._window_updater = WindowUpdater(self._elements_dict)

    def _init_board(self):
        board = self._game.board

        # create ending button
        end_button = Button()
        label = CommonFontLabel(font_modificator=0.08, text="Zakończ grę")
        end_button.add_widget(label)
        end_button.bind(size=label.setter("size"))
        end_button.bind(pos=label.setter("pos"))
        end_button.bind(on_press=self._show_end_popup)
        self._elements_dict.get("button_tab").add_widget(end_button)

        # assigning observer to game
        self._game.add_observer(self);

        # creation of indicator dots
        for i in range(len(self._dots)):
            self._dots[i] = Image(source=f"{Path.WOODEN_IMG_PATH}/highlight_bg.png")
            self._dots[i].allow_stretch = True
            self._dots[i].texture.mag_filter = "nearest"

        # creation of laser dots
        # for i in range(len(self._laser_ind)):
        #     self._laser_ind[i] = Image(source=f"{Path.IMG_PATH}/lasgun_dot.png")

        self._add_coordinates()

        self.update_indicator_label("Gracz " + str(self._board.move_number))

        #
        # Cell buttons of the board
        #
        for i in range(8):
            for j in range(8):
                vector = BoardVector2d(j, 7 - i)

                # preparation of every button on board
                button = Button()
                button.vector = vector
                button.bind(on_press=self.on_tile_click)

                button.background_normal = ""
                if (i + j) % 2 == 0:
                    img = Image(source=f"{Path.WOODEN_IMG_PATH}/bg_light.png")
                    # button.background_color = rgba_int_to_float((150, 50, 50, 255))
                else:
                    img = Image(source=f"{Path.WOODEN_IMG_PATH}/bg_dark.png")
                    # button.background_color = rgba_int_to_float((54, 54, 54, 255))
                img.size_hint = (1, 1)
                img.allow_stretch = True
                img.texture.mag_filter = "nearest"
                self._elements_dict["board_images"][i, j] = img
                button.add_widget(img)

                # assigning observer to piece
                piece = board.get_piece(vector)
                if piece is not None:
                    piece.add_observer(self)
                    if piece.model == PieceModel.LASGUN:
                        piece.add_laser_observer(self)

                # adding piece and button to board
                piece_layout = PieceRepresentationLayout(piece, button)
                self._grid.add_widget(piece_layout)
                self._representations[vector.y][vector.x] = piece_layout

        # creation of promotion tab
        self._promotion_representation = [
            PieceRepresentationLayout(None, Button(on_press=self.on_promotion_click)) for _ in
            self._board.get_possible_promotions()
        ]
        # for e in self._promotion_representation:
        #     e.size_hint = (None, None)

        # creation of rotation tab

        self._rotation_representation = [
            ImageButtonLayout(Paths.LEFT.value, Button(on_press=self.on_rotation_click)),
            ImageButtonLayout(Paths.RIGHT.value, Button(on_press=self.on_rotation_click))
        ]

        for e in self._rotation_representation:
            e.size_hint = (None, None)

        r = self._rotation_representation
        r[0].add_value_to_button(Paths.LEFT)
        r[1].add_value_to_button(Paths.RIGHT)

    def _add_coordinates(self):
        boxes = [self.ids.top, self.ids.left, self.ids.bot, self.ids.right]
        for i in range(8):
            for j in range(4):
                label = CommonFontLabel(font_modificator=0.4)
                # CommonFontLabel.update_font(20)
                if j % 2 == 1:
                    label.text = str(8 - i)
                else:
                    label.text = chr(i + 97)
                label.bold = True
                boxes[j].add_widget(label)

    def _show_end_popup(self, instance):
        popup = Popup(size_hint=(0.6, 0.2), auto_dismiss=False)
        title = "Koniec gry. Wygrał ..."
        content = Button(text="Zakończ")
        if isinstance(instance, Button):
            title = 'Czy na pewno chcesz zakończyć rozgrywkę?'
            content = BoxLayout(orientation="horizontal", padding=20, size_hint=(1, 1))
            no = Button(text="Nie", size_hint=(0.5, 0.5))
            yes = Button(text="Tak", size_hint=(0.5, 0.5))
            content.add_widget(yes)
            content.add_widget(no)
            yes.bind(on_press=lambda x: popup.dismiss())
            no.bind(on_press=popup.dismiss)
        popup.title = title
        popup.size_hint_min = (200, 200)
        popup.size_hint_max = (300, 300)
        popup.content = content
        popup.open()
        if isinstance(instance, Button):
            yes.bind(on_press=lambda x: popup.dismiss())
            no.bind(on_press=popup.dismiss)

    def _show_checks(self):
        for king in self._board.kings:
            if self._board.is_king_under_check(king.player_id):
                check = Image(source=f"{Path.IMG_PATH}/this_fire.png")
                vector = king.position
                self._representations[vector.y][vector.x].add_indicator(check)

    def _update(self):
        for i in range(len(self._representations)):
            for j in range(len(self._representations[i])):
                self._representations[i][j].remove_indicator()
                self._representations[i][j].remove_img()
                self._representations[i][j].new_image_piece(self._board.get_piece(BoardVector2d(j, i)))
        self._show_indicators()
        self._laser_painer.clear()
        self._laser_painer.paint()
        self._window_updater.refresh()

    def get_to_promote(self):
        return self._promotion.get_promotion_piece()

    def on_rotation_click(self, instance: Button):
        match instance.value:
            case Paths.LEFT:
                self._game.move_piece(self._selected_piece, None, Rotation.ANTICLOCKWISE)
            case Paths.RIGHT:
                self._game.move_piece(self._selected_piece, None, Rotation.CLOCKWISE)
        self.hide_rotation_menu()
        self.on_tile_click(self._reset_button)
        self._possible_movements = []
        self._selected = None
        self._selected_piece = None
        self._game_app.on_move()

    def on_tile_click(self, instance: Button):
        self.hide_rotation_menu()
        if self._is_promotion:
            return

        # clear indicating dots

        for d in self._current_dots:
            d.parent.remove_widget(d)
        self._current_dots.clear()

        piece = self._board.get_piece(instance.vector)
        if piece is None and instance.vector not in self._possible_movements:
            self._possible_movements.clear()
        if piece is not None and piece.is_same_color(self._board.move_number):
            if piece.model == PieceModel.LASGUN:
                self._board.laser_fire_conditions(piece.player_id)
                return
            self._selected_piece = self._board.get_piece(instance.vector)
            self._selected = self._board.get_piece_movement(instance.vector)
            self._possible_movements = list(itertools.chain.from_iterable(self._selected.get_legal_moves()))
            self.on_show_possible_movements(self._possible_movements)
            if piece.model == PieceModel.MIRROR and not self._board.is_king_under_check(piece.player_id):
                self.show_rotation_menu()

        #
        # Move piece
        #
        if self._selected is not None and instance.vector in self._possible_movements:
            asyncio.run(self.__move_piece(instance.vector))

    def on_show_possible_movements(self, fields: list[BoardVector2d]):
        i = 0
        for m in fields:
            self._representations[m.y][m.x].add_widget(self._dots[i])
            self._current_dots.append(self._dots[i])
            i += 1

    def on_show_laser_fields(self, movements: list[BoardVector2d], player_id: int):
        i = 0
        for m in movements:
            self._representations[m.y][m.x].add_widget(self._laser_ind[i])
            self._current_laser_ind.append(self._laser_ind[i])
            i += 1

    def on_promotion_click(self, instance: Button):
        new = self._board.promote(instance.value)
        new[0].add_observer(self)
        self.hide_promotion_menu()
        self._is_promotion = False
        self._update()
        self._update_notation()
        # self.on_position_change(None, None)

    # override
    def on_position_change(self, origin: BoardVector2d, destination: BoardVector2d) -> None:
        self._update()
        if PieceMoveType.PROMOTION not in self._game.get_last_move().move_types:
            self._update_notation()

    def on_laser_propagated(self, lasgun: Lasgun):
        self._update()
        # self._update_notation()

    def on_rotation(self, origin: BoardVector2d, rotation: Paths) -> None:
        self._update()
        self._update_notation()

    async def __move_piece(self, destination: BoardVector2d) -> None:
        self.update_indicator_label("Player " + str(self._board.move_number))
        self._game.move_piece(self._selected_piece, destination)
        await self._game_app.on_move()
        self.show_promotion_menu(self._board.get_to_promote())
        self._possible_movements.clear()
        self._selected = None
        self._selected_piece = None

    def _update_notation(self):
        def size(instance, val):
            instance.height = val

        def size2(instance, val):
            instance.text_size = val[0], val[1]

        not_tab = self._elements_dict.get('notation')
        notation = self._game._notation_generator.generate_last_move_string()
        self._notation_list.append(notation)
        if len(self._notation_list) % 2 == 1:
            notation = str(len(self._notation_list) // 2 + 1) + "." + notation
            print(notation)

        l = CommonFontLabel(halign="left", font_modificator=0.15, size_hint=(1, None), text=notation)
        l.bind(font_size=size)
        l.bind(size=size2)
        not_tab.add_widget(l)
        scroll = self._elements_dict.get("scroll")
        if scroll.children[0].height > scroll.height:
            scroll.scroll_to(l)

    def _show_lasgun_ready_indicators(self):
        for las in self._board.lasguns:
            if las.can_fire():
                ready = Image(source=f"{Path.IMG_PATH}/laser_ready.png")
                vector = las.position
                self._representations[vector.y][vector.x].add_indicator(ready)

    def _show_indicators(self):
        self._show_checks()
        self._show_lasgun_ready_indicators()

    # override
    def on_end(self, winner: int, type: PieceMoveType) -> None:
        self.update_indicator_label("Wygrywa " + str(winner))
        for rep_arr in self._representations:
            for rep in rep_arr:
                cast(PieceRepresentationLayout, rep).button.unbind(on_press=self.on_tile_click)

    def update_indicator_label(self, text: str):
        self._indicator_label.text = text
        pass

    def show_rotation_menu(self):
        tab = self._elements_dict.get('rotation_promotion_tab')
        for rep in self._rotation_representation:
            tab.add_widget(rep)
        self._window_updater.refresh()

    def hide_rotation_menu(self):
        for rep in self._rotation_representation:
            if rep.parent is not None:
                rep.parent.remove_widget(rep)
        self._window_updater.refresh()

    def show_promotion_menu(self, piece: Piece):
        tab = self._elements_dict.get('rotation_promotion_tab')
        types = self._board.get_possible_promotions()
        if piece is None:
            return
        self._is_promotion = True
        grid = GridLayout(cols=2)
        for rep, tp in zip(self._promotion_representation, types):
            rep.add_value_to_button(tp)
            rep.new_image(tp, piece.player_id)
            grid.add_widget(rep)
        tab.add_widget(grid)
        self._window_updater.refresh()

    def hide_promotion_menu(self):
        prom = self._promotion_representation
        if len(prom) > 0:
            prom[0].parent.parent.remove_widget(prom[0].parent)
        for rep in prom:
            if rep.parent is not None:
                rep.parent.remove_widget(rep)
        self._window_updater.refresh()
