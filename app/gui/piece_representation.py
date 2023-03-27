from kivy.uix.image import Image
from game.pieces.piece_model import PieceModel


# 0-white
class PieceRepresentation:
    def __init__(self, piece_type: PieceModel, player: int):
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
                        self._img = Image(source="assets/b_queeen.png")
                    case piece_type.MIRROR:
                        self._img = Image(source="assets/b_mirror.png")

    def get_representation(self):
        return self._img



