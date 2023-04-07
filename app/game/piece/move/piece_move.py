from utils import Vector2d
import game.piece as pcs


class PieceMove:
    def __init__(self, move_index: int, piece: pcs.Piece, origin: Vector2d, destination: Vector2d) -> None:
        self.move: int = move_index
        self.piece: pcs.Piece = piece
        self.origin: Vector2d = origin
        self.destination: Vector2d = destination
