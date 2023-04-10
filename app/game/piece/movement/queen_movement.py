from __future__ import annotations
from typing import TYPE_CHECKING
from utils import Vector2d
from game.piece.movement import BishopMovement, RookMovement

if TYPE_CHECKING:
    from game import Board
    from game.piece import Piece


class QueenMovement(BishopMovement, RookMovement):
    def __init__(self, queen: Piece, board: Board) -> None:
        super().__init__(queen, board)

    def get_legal_moves(self) -> list[list[Vector2d]]:
        super().get_legal_moves()
        # BishopMovement.get_legal_moves(self)
        tmp_legal = self._legal_moves.copy()
        RookMovement.get_legal_moves(self)
        self._legal_moves.extend(tmp_legal)

        return self._legal_moves
