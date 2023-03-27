from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout

from game.pieces.piece import Piece
from utils.vector2d import Vector2d



# 0-white
class PieceRepresentationLayout(RelativeLayout):
    def __init__(self, piece: Piece,button: Button):
        super().__init__()
        self.add_widget(button)
        if piece is None:
            self._img = None
            return
        piece_type = piece.model
        player = piece.player_id
        self._img = None
        match player:
            case 0:
                match piece_type:
                    case piece_type.PAWN:
                        self._img = Image(source="assets/w_pawn.png")
                    case piece_type.KNIGHT:
                        self._img = Image(source="assets/w_knight.png")
                    case piece_type.ROOK:
                        self._img = Image(source="assets/w_rook.png")
                    case piece_type.BISHOP:
                        self._img = Image(source="assets/w_bishop.png")
                    case piece_type.QUEEN:
                        self._img = Image(source="assets/w_queen.png")
                    case piece_type.MIRROR:
                        self._img = Image(source="assets/w_mirror.png")
                    case _:
                        self._img = None

            case 1:
                match piece_type:
                    case piece_type.PAWN:
                        self._img = Image(source="assets/b_pawn.png")
                    case piece_type.KNIGHT:
                        self._img = Image(source="assets/b_knight.png")
                    case piece_type.ROOK:
                        self._img = Image(source="assets/b_rook.png")
                    case piece_type.BISHOP:
                        self._img = Image(source="assets/b_bishop.png")
                    case piece_type.QUEEN:
                        self._img = Image(source="assets/b_queen.png")
                    case piece_type.MIRROR:
                        self._img = Image(source="assets/b_mirror.png")
                    case _:
                        self._img = None
        self.add_widget(self._img)

    def remove_img(self) -> Image:
        if self._img is None:
            return None
        img = self._img
        self._img = None
        self.remove_widget(img)
        return img
    def add_img(self, img: Image):
        self._img = img
        self.add_widget(img)

