from __future__ import annotations
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from typing import cast

from app.gui import Path
from game.piece import PieceModel
from game.piece.lasgun import MirrorPiece
from game.piece.movement import Movement
from game.piece.piece import Piece


# 0-white
class PieceRepresentationLayout(RelativeLayout):
    def __init__(self, piece: Piece | None, button: Button, opacity=None, promotion=None):
        super().__init__()
        print(Path.PIECE_IMG_PATH)
        self._button = button
        self.add_widget(button)
        self._img = None
        self._indicator = None
        self._piece = piece

        if opacity is not None:
            self.opacity = opacity
        if piece is None:
            return

        self.__load(piece.model,piece.player_id)
        self.__add_img_to_repr(self._img)

    def __load(self, piece_type: PieceModel, player: int):
        if piece_type is None or player is None:
            self._img = None
            return

        color = ""
        match player:
            case 0:
                color = "w"
            case 1:
                color = "b"

        match piece_type:
            case piece_type.KING:
                self._img = Image(source=f"{Path.PIECE_IMG_PATH}/{color}_king.png")
            case piece_type.QUEEN:
                self._img = Image(source=f"{Path.PIECE_IMG_PATH}/{color}_queen.png")
            case piece_type.PAWN:
                self._img = Image(source=f"{Path.PIECE_IMG_PATH}/{color}_pawn.png")
            case piece_type.KNIGHT:
                self._img = Image(source=f"{Path.PIECE_IMG_PATH}/{color}_knight.png")
            case piece_type.ROOK:
                self._img = Image(source=f"{Path.PIECE_IMG_PATH}/{color}_rook.png")
            case piece_type.BISHOP:
                self._img = Image(source=f"{Path.PIECE_IMG_PATH}/{color}_bishop.png")
            case piece_type.LASGUN:
                self._img = Image(source=f"{Path.PIECE_IMG_PATH}/{color}_lasgun.png")
            case piece_type.MIRROR:
                match cast(MirrorPiece, self._piece).direction:
                    case Movement.UPPER_LEFT_DIAGONAL:
                        rotation = "ul"
                    case Movement.UPPER_RIGHT_DIAGONAL:
                        rotation = "ur"
                    case Movement.BOTTOM_RIGHT_DIAGONAL:
                        rotation = "br"
                    case Movement.BOTTOM_LEFT_DIAGONAL:
                        rotation = "bl"
                    case _:
                        rotation = "bl"
                self._img = Image(source=f"{Path.PIECE_IMG_PATH}/{color}_{rotation}_mirror.png")
                self._img.allow_stretch = True
                self._img.keep_ratio = False
            case _:
                self._img = None

    def __add_img_to_repr(self, img: Image):
        self.add_widget(img)

    def add_value_to_button(self, value):
        self._button.value = value

    def remove_img(self) -> Image | None:
        if self._img is None:
            return None
        img = self._img
        self.remove_widget(img)
        self._img = None
        return img

    def new_image_piece(self, piece: Piece):
        if piece is None:
            return
        self._piece = piece
        self.__load(piece.model, piece.player_id)
        self.__add_img_to_repr(self._img)

    def new_image(self, model: PieceModel, player: int):
        self._piece = None
        if model is None or player is None:
            return
        self.__load(model, player)
        self.__add_img_to_repr(self._img)
        pass

    def add_indicator(self, img: Image):
        if self._indicator is not None:
            return
        self._indicator = img
        img.size_hint = (0.5, 0.5)
        self.__add_img_to_repr(img)

    def remove_indicator(self):
        if self._indicator is None:
            return None
        img = self._indicator
        self.remove_widget(self._indicator)
        self._indicator = None
        return img

    # not used (yet)

    def replace_indicator(self, img: Image):
        self.remove_indicator()
        self.add_indicator(img)

    def add_img(self, img: Image):
        if self._img is not None:
            return
        self._img = img
        self.__add_img_to_repr(img)