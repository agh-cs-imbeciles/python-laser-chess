from __future__ import annotations
from typing import TYPE_CHECKING
from utils import BoardVector2d
from game.piece.movement import Movement, RangedPieceMovement

if TYPE_CHECKING:
    from game import Board
    from game.piece import Piece


class RookMovement(RangedPieceMovement):
    # Movement types, (movement, delta)
    # movement: movement type
    # delta: delta position of the piece, position + delta is the origin of iteration
    movements: list[tuple[Movement, BoardVector2d]] = [
        (Movement.UPPER_FILE, BoardVector2d(0, 1)),
        (Movement.BOTTOM_FILE, BoardVector2d(0, -1)),
        (Movement.LEFT_RANK, BoardVector2d(-1, 0)),
        (Movement.RIGHT_RANK, BoardVector2d(1, 0)),
    ]

    def __init__(self, rook: Piece, board: Board) -> None:
        super().__init__(rook, board)
        self._movements: list[tuple[Movement, BoardVector2d]] = RookMovement.movements
