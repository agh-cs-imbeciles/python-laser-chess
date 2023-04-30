from __future__ import annotations
from abc import ABC, abstractmethod


class BaseBoardCoord(ABC):
    def __init__(self, value: int) -> None:
        self.value: int = value

    def __eq__(self, other) -> bool:
        if not isinstance(other, BaseBoardCoord):
            return False
        return self.value == other.value

    def __ne__(self, other) -> bool:
        return not self == other

    def __hash__(self):
        return hash(self.value)

    # def __add__(self, other: BaseBoardCoord | int) -> BaseBoardCoord:
    #     if isinstance(other, BaseBoardCoord):
    #         return BaseBoardCoord(self.value + other.value)
    #
    # def __sub__(self, other: Vector2d) -> Vector2d:
    #     return Vector2d(self.x - other.x, self.y - other.y)
    #
    # def __mul__(self, other: Vector2d) -> Vector2d:
    #     return Vector2d(self.x * other.x, self.y * other.y)
    #
    # def __truediv__(self, other: Vector2d) -> Vector2d:
    #     if other.x == 0:
    #         raise ZeroDivisionError("The 2nd argument x is equal 0")
    #     if other.y == 0:
    #         raise ZeroDivisionError("The 2nd argument y is equal 0")
    #
    #     return Vector2d(self.x // other.x, self.y // other.y)

    @property
    def value(self) -> int:
        return self._value

    @value.setter
    def value(self, value: int):
        self._value = value


class File(BaseBoardCoord):
    # override
    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        return isinstance(other, File)

    def __str__(self) -> str:
        return str(self._value + 1)


class Rank(BaseBoardCoord):
    # override
    def __eq__(self, other):
        if not super().__eq__(other):
            return False
        return isinstance(other, Rank)

    def __str__(self) -> str:
        return chr(self._value + 97)
