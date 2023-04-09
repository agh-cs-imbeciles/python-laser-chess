from __future__ import annotations
from typing import TYPE_CHECKING
from utils import Vector2d
from game.piece.movement import Movement, PieceMovement

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
        # Upper file
        #
        self._legal_moves += b.check_squares(p, p.position + Vector2d(0, 1), Movement.UPPER_FILE)
        #
        # Bottom file
        #
        self._legal_moves += b.check_squares(p, p.position + Vector2d(0, -1), Movement.BOTTOM_FILE)
        #
        # Left rank
        #
        self._legal_moves += b.check_squares(p, p.position + Vector2d(-1, 0), Movement.LEFT_RANK)
        #
        # Right rank
        #
        self._legal_moves += b.check_squares(p, p.position + Vector2d(1, 0), Movement.RIGHT_RANK)

        return self._legal_moves
