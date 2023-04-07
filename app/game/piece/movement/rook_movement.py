from __future__ import annotations
from typing import TYPE_CHECKING
from utils import Vector2d
from game.piece.movement import PieceMovement

if TYPE_CHECKING:
    from game import Board
    from game.piece import Piece


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
        self._legal_moves += b.check_squares(p, p.position + Vector2d(0, 1), Vector2d(0, b.height), (0, 1))
        #
        # Bottom line
        #
        self._legal_moves += b.check_squares(p, p.position + Vector2d(0, -1), Vector2d(0, -1), (0, -1))
        #
        # Left line
        #
        self._legal_moves += b.check_squares(p, p.position + Vector2d(-1, 0), Vector2d(-1, 0), (-1, 0))
        #
        # Right line
        #
        self._legal_moves += b.check_squares(p, p.position + Vector2d(1, 0), Vector2d(b.width, 0), (1, 0))

        return self._legal_moves