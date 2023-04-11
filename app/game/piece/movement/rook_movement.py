from __future__ import annotations
from typing import TYPE_CHECKING
from utils import Vector2d
from game.piece.movement import Movement, RangePieceMovement

if TYPE_CHECKING:
    from game import Board
    from game.piece import Piece


class RookMovement(RangePieceMovement):
    def __init__(self, rook: Piece, board: Board) -> None:
        super().__init__(rook, board)

    # override
    def get_legal_moves(self) -> list[list[Vector2d]]:
        self._legal_moves.clear()
        p = self._piece

        #
        # Upper file
        #
        self._legal_moves.append(self.iterate_squares(p.position + Vector2d(0, 1), Movement.UPPER_FILE)[0])
        #
        # Bottom file
        #
        self._legal_moves.append(self.iterate_squares(p.position + Vector2d(0, -1), Movement.BOTTOM_FILE)[0])
        #
        # Left rank
        #
        self._legal_moves.append(self.iterate_squares(p.position + Vector2d(-1, 0), Movement.LEFT_RANK)[0])
        #
        # Right rank
        #
        self._legal_moves.append(self.iterate_squares(p.position + Vector2d(1, 0), Movement.RIGHT_RANK)[0])

        return self._legal_moves
