from __future__ import annotations
from typing import TYPE_CHECKING
from utils import Vector2d
from game.pieces.movement import PieceMovement

if TYPE_CHECKING:
    from game import Board
    from game.pieces import Piece


class RookMovement(PieceMovement):
    def __init__(self, rook: Piece, board: Board) -> None:
        super().__init__(rook, board)

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
