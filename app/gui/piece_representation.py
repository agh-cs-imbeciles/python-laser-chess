from __future__ import annotations
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout

from game.piece import PieceModel
from game.piece.piece import Piece


# 0-white
class PieceRepresentationLayout(RelativeLayout):
    def __init__(self, piece: Piece, button: Button,opacity=None,promotion=None):
        super().__init__()
        self._button = button
        self.add_widget(button)
        self._img = None
        self._indicator = None
        if opacity is not None:
            self.opacity = opacity
        if piece is None:
            return
        self.__load(piece.model,piece.player_id)
        self.add_widget(self._img)


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
                self._img = Image(source=f"assets/{color}_king.png")
            case piece_type.QUEEN:
                self._img = Image(source=f"assets/{color}_queen.png")
            case piece_type.PAWN:
                self._img = Image(source=f"assets/{color}_pawn.png")
            case piece_type.KNIGHT:
                self._img = Image(source=f"assets/{color}_knight.png")
            case piece_type.ROOK:
                self._img = Image(source=f"assets/{color}_rook.png")
            case piece_type.BISHOP:
                self._img = Image(source=f"assets/{color}_bishop.png")
            case piece_type.MIRROR:
                self._img = Image(source=f"assets/{color}_mirror.png")
            case _:
                self._img = None

    def add_value_to_button(self,value):
        self._button.value = value

    def remove_img(self) -> Image | None:
        if self._img is None:
            return None
        img = self._img
        self.remove_widget(img)
        self._img = None
        return img

    def add_img(self, img: Image):
        if self._img is not None:
            return
        self._img = img
        self.add_widget(img)


    def new_image_piece(self, piece: Piece):
        if piece is None:
            return
        self.__load(piece.model, piece.player_id)
        self.add_widget(self._img)

    def new_image(self, model: PieceModel, player: int):
        if model is None or player is None:
            return
        self.__load(model, player)
        self.add_widget(self._img)
        pass

    def add_indicator(self, img: Image):
        if self._indicator is not None:
            return
        self._indicator = img
        img.size_hint = (0.5, 0.5)
        self.add_widget(img)

    def remove_indicator(self):
        if self._indicator is None:
            return None
        img = self._indicator
        self.remove_widget(self._indicator)
        self._indicator = None
        return img

    def replace_indicator(self, img: Image):
        self.remove_indicator()
        self.add_indicator(img)
