from __future__ import annotations
from typing import TYPE_CHECKING
from game.pieces.movement import PieceMovement
from utils import Vector2d

if TYPE_CHECKING:
    from game.pieces.piece import Piece
    from game.board import Board


class BishopMovement(PieceMovement):
    def __init__(self, bishop: Piece, board: Board) -> None:
        super().__init__(bishop, board)

    # override
    def get_legal_moves(self) -> list[Vector2d]:
        self._legal_moves.clear()
        b = self._board
        p = self._piece

        #
        # Upper right diagonal
        #
        self.check_squares(p, b, p.position + Vector2d(1, 1), Vector2d(b.width, b.height), (1, 1))
        #
        # Bottom left diagonal
        #
        self.check_squares(p, b, p.position + Vector2d(-1, -1), Vector2d(-1, -1), (-1, -1))
        #
        # Upper left diagonal
        #
        self.check_squares(p, b, p.position + Vector2d(-1, 1), Vector2d(-1, b.height), (-1, 1))
        #
        # Bottom right diagonal
        #
        self.check_squares(p, b, p.position + Vector2d(1, -1), Vector2d(b.width, -1), (1, -1))

        return self._legal_moves
