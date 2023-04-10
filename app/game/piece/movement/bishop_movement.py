from __future__ import annotations
from typing import TYPE_CHECKING
from utils import Vector2d
from game.piece.movement import Movement, PieceMovement

if TYPE_CHECKING:
    from game.piece.piece import Piece
    from game.board import Board


class BishopMovement(PieceMovement):
    def __init__(self, bishop: Piece, board: Board) -> None:
        super().__init__(bishop, board)

    # override
    def get_legal_moves(self) -> list[list[Vector2d]]:
        self._legal_moves.clear()
        b = self._board
        p = self._piece

        #
        # Upper right diagonal
        #
        self._legal_moves.append(b.check_squares(p, p.position + Vector2d(1, 1), Movement.UPPER_RIGHT_DIAGONAL))
        #
        # Bottom left diagonal
        #
        self._legal_moves.append(b.check_squares(p, p.position + Vector2d(-1, -1), Movement.BOTTOM_LEFT_DIAGONAL))
        #
        # Upper left diagonal
        #
        self._legal_moves.append(b.check_squares(p, p.position + Vector2d(-1, 1), Movement.UPPER_LEFT_DIAGONAL))
        #
        # Bottom right diagonal
        #
        self._legal_moves.append(b.check_squares(p, p.position + Vector2d(1, -1), Movement.BOTTOM_RIGHT_DIAGONAL))

        return self._legal_moves
