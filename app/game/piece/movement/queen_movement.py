from __future__ import annotations
from copy import deepcopy
from typing import TYPE_CHECKING
from utils import Vector2d
from game.piece.movement import BishopMovement, RookMovement, RangePieceMovement

if TYPE_CHECKING:
    from game import Board
    from game.piece import Piece


class QueenMovement(RangePieceMovement):
    def __init__(self, queen: Piece, board: Board) -> None:
        super().__init__(queen, board)
        self._movements = BishopMovement.movements + RookMovement.movements
