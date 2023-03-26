from bishop_movement import BishopMovement
from rook_movement import RookMovement
from game.pieces.piece import Piece
from game.board import Board
from utils.vector2d import Vector2d


class QueenMovement(BishopMovement, RookMovement):
    def __init__(self, pawn: Piece, board: Board) -> None:
        super().__init__(pawn, board)

    def get_legal_moves(self) -> list[Vector2d]:
        super().get_legal_moves()
        return self._legal_moves
