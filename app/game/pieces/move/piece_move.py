from utils.vector2d import Vector2d
from game.pieces.piece import Piece


class PieceMove:
    def __init__(self, move_index: int, piece: Piece, from_p: Vector2d, to_p: Vector2d):
        self.move: int = move_index
        self.piece: Piece = piece
        self.from_p: Vector2d = from_p
        self.to_p: Vector2d = to_p
