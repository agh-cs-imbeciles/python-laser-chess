from __future__ import annotations
from typing import TYPE_CHECKING
from utils import Vector2d
from game.piece import PieceModel
from game.piece.movement import Movement, RangePieceMovement

if TYPE_CHECKING:
    from game.piece.piece import Piece
    from game.board import Board


class BishopMovement(RangePieceMovement):
    # Movement types, (movement, delta)
    # movement: movement type
    # delta: delta position of the piece, position + delta is the origin of iteration
    movements: list[tuple[Movement, Vector2d]] = [
        (Movement.UPPER_RIGHT_DIAGONAL, Vector2d(1, 1)),
        (Movement.BOTTOM_LEFT_DIAGONAL, Vector2d(-1, -1)),
        (Movement.UPPER_LEFT_DIAGONAL, Vector2d(-1, 1)),
        (Movement.BOTTOM_RIGHT_DIAGONAL, Vector2d(1, -1)),
    ]

    def __init__(self, bishop: Piece, board: Board) -> None:
        super().__init__(bishop, board)
        self._movements = BishopMovement.movements
