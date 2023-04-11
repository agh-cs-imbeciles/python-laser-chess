from __future__ import annotations
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from game.piece.piece import Piece


# 0-white
class PieceRepresentationLayout(RelativeLayout):
    def __init__(self, piece: Piece, button: Button):
        super().__init__()
        self.add_widget(button)
        self._img = None
        self._indicator = None
        if piece is None:
            return
        self.__load(piece)
        self.add_widget(self._img)

    def __load(self, piece: Piece):
        if piece is None:
            self._img = None
            return
        piece_type = piece.model
        player = piece.player_id
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

    def remove_img(self) -> Image | None:
        if self._img is None:
            return None
        img = self._img
        self.remove_widget(img)
        self._img = None
        return img

    def add_img(self, img: Image):
        self._img = img
        self.add_widget(img)

    def new_image(self, piece: Piece):
        if piece is None:
            return
        self.__load(piece)
        self.add_widget(self._img)

    def add_indicator(self, img: Image):
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
