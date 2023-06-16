from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING
from utils import BoardVector2d

if TYPE_CHECKING:
    from game import Board


class Movement(Enum):
    LEFT_RANK               = 0
    UPPER_LEFT_DIAGONAL     = 1
    UPPER_FILE              = 2
    UPPER_RIGHT_DIAGONAL    = 3
    RIGHT_RANK              = 4
    BOTTOM_RIGHT_DIAGONAL   = 5
    BOTTOM_FILE             = 6
    BOTTOM_LEFT_DIAGONAL    = 7

    def left(self) -> Movement:
        return Movement((self.value-1) % 8)

    def double_left(self) -> Movement:
        return self.left().left()

    def right(self) -> Movement:
        return Movement((self.value+1) % 8)

    def double_right(self) -> Movement:
        return self.right().right()

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
    def get_squares_from_tuple(cls, increment: tuple[int, int], board: Board, origin: BoardVector2d) -> list[BoardVector2d]:
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
        moves = [BoardVector2d(x, y) for x, y in zip(xs, ys)]
        filtered = []
        for m in moves:
            if m in board.get_laser_fields():
                break
            filtered.append(m)
        return filtered

    @classmethod
    def get_squares(cls, movement: Movement, board: Board, origin: BoardVector2d) -> list[BoardVector2d]:
        return Movement.get_squares_from_tuple(movement.to_tuple(), board, origin)
