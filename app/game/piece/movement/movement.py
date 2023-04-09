from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING
from utils import Vector2d

if TYPE_CHECKING:
    from game import Board


class Movement(Enum):
    RANK                    = 0,
    FILE                    = 1,
    DIAGONAL                = 2,
    LEFT_RANK               = 3,
    RIGHT_RANK              = 4,
    UPPER_FILE              = 5,
    BOTTOM_FILE             = 6,
    UPPER_LEFT_DIAGONAL     = 7,
    UPPER_RIGHT_DIAGONAL    = 8,
    BOTTOM_RIGHT_DIAGONAL   = 9,
    BOTTOM_LEFT_DIAGONAL    = 10

    def to_tuple(self) -> tuple[int, int]:
        """
        Returns right increment tuple from Movement enum.
        :param movement: Movement
        :return: tuple[int, int]
        """

        match self:
            case Movement.LEFT_RANK:
                return -1, 0
            case Movement.RIGHT_RANK:
                return 1, 0
            case Movement.UPPER_FILE:
                return 0, 1
            case Movement.BOTTOM_FILE:
                return 0, -1
            case Movement.UPPER_LEFT_DIAGONAL:
                return -1, 1
            case Movement.UPPER_RIGHT_DIAGONAL:
                return 1, 1
            case Movement.BOTTOM_RIGHT_DIAGONAL:
                return 1, -1
            case Movement.BOTTOM_LEFT_DIAGONAL:
                return -1, -1
            case _:
                raise ValueError("Invalid movement parameter")

    @classmethod
    def get_squares_from_tuple(cls, increment: tuple[int, int], board: Board, origin: Vector2d) -> list[Vector2d]:
        xi, yi = increment
        if xi == 0 and yi == 0:
            raise ValueError("increment tuple must be different than (0, 0)")

        xs, ys = [], []
        if xi != 0:
            xs = [x for x in range(origin.x, board.width if xi > 0 else -1, xi)]
        if yi != 0:
            ys = [y for y in range(origin.y, board.width if yi > 0 else -1, yi)]
        if xi == 0:
            xs = [origin.x for _ in ys]
        if yi == 0:
            ys = [origin.y for _ in xs]

        return [Vector2d(x, y) for x, y in zip(xs, ys)]

    @classmethod
    def get_squares(cls, movement: Movement, board: Board, origin: Vector2d) -> list[Vector2d]:
        return Movement.get_squares_from_tuple(movement.to_tuple(), board, origin)
