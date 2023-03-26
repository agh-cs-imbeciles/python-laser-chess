from utils.vector2d import Vector2d
from game.pieces.piece import Piece


class PieceMove:
    def __init__(self, move_index: int, piece: Piece, origin: Vector2d, destination: Vector2d) -> None:
        self.move: int = move_index
        self.piece: Piece = piece
        self.origin: Vector2d = origin
        self.destination: Vector2d = destination
