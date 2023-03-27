from __future__ import annotations
from typing import TYPE_CHECKING
from utils import Vector2d
from game.pieces.movement import BishopMovement, RookMovement

if TYPE_CHECKING:
    from game import Board
    from game.pieces import Piece


class QueenMovement(BishopMovement, RookMovement):
    def __init__(self, pawn: Piece, board: Board) -> None:
        super().__init__(pawn, board)

    def get_legal_moves(self) -> list[Vector2d]:
        super().get_legal_moves()
        return self._legal_moves
