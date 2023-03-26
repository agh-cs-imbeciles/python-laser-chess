from typing import Tuple
from piece_movement import PieceMovement
from game.pieces.piece import Piece
from game.board import Board
from utils.vector2d import Vector2d


class RookMovement(PieceMovement):
    def __init__(self, pawn: Piece, board: Board) -> None:
        super().__init__(pawn, board)

    # override
    def get_legal_moves(self) -> list[Vector2d]:
        self._legal_moves.clear()
        b = self._board
        p = self._piece

        #
        # Upper line
        #
        self.check_squares(p, b, p.position + Vector2d(0, 1), Vector2d(0, b.height), (0, 1))
        #
        # Bottom line
        #
        self.check_squares(p, b, p.position + Vector2d(0, -1), Vector2d(0, -1), (0, -1))
        #
        # Left line
        #
        self.check_squares(p, b, p.position + Vector2d(-1, 0), Vector2d(-1, 0), (-1, 0))
        #
        # Right line
        #
        self.check_squares(p, b, p.position + Vector2d(1, 0), Vector2d(b.width, 0), (1, 0))

        return self._legal_moves
