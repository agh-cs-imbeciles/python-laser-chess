from __future__ import annotations
from enum import Enum
from typing import TypeVar, Generic


X = TypeVar('X')
Y = TypeVar('Y')


class Symmetry(Enum):
    ORIGIN  = 0,
    X_AXIS  = 1,
    Y_AXIS  = 2


class Vector2d(Generic[X, Y]):
    def __init__(self, x: X, y: Y):
        self._x: X = x
        self._y: Y = y

    @property
    def x(self) -> X:
        return self._x

    @x.setter
    def x(self, x: X) -> None:
        self._x = x

    @property
    def y(self) -> Y:
        return self._y

    @y.setter
    def y(self, y: Y) -> None:
        self._y = y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __iter__(self) -> tuple[X, Y]:
        return self.x, self.y

    def __eq__(self, other) -> bool:
        if not isinstance(other, Vector2d):
            return False
        return self.x == other.x and self.y == other.y

    def __ne__(self, other) -> bool:
        return not self == other

    def __add__(self, other: Vector2d[X, Y]) -> Vector2d[X, Y]:
        return Vector2d[X, Y](self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2d[X, Y]) -> Vector2d[X, Y]:
        return Vector2d[X, Y](self.x - other.x, self.y - other.y)

    def __mul__(self, other: Vector2d[X, Y]) -> Vector2d[X, Y]:
        return Vector2d[X, Y](self.x * other.x, self.y * other.y)

    def __floordiv__(self, other) -> Vector2d[X, Y]:
        if other.x == 0:
            raise ZeroDivisionError("The x of other vector is equal 0")
        if other.y == 0:
            raise ZeroDivisionError("The y of other vector is equal 0")

        return Vector2d[X, Y](self.x // other.x, self.y // other.y)

    def __truediv__(self, other: Vector2d[X, Y]) -> Vector2d[X, Y]:
        if other.x == 0:
            raise ZeroDivisionError("The x of other vector is equal 0")
        if other.y == 0:
            raise ZeroDivisionError("The y of other vector is equal 0")

        return Vector2d[X, Y](self.x / other.x, self.y / other.y)

    def __neg__(self) -> Vector2d[X, Y]:
        return Vector2d[X, Y](-self.x, -self.y)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def multiply_scalar(self, scalar: float) -> Vector2d[X, Y]:
        return Vector2d[X, Y](X(self.x * scalar), Y(self.y * scalar))

    def reverse_axis(self) -> Vector2d[X, Y]:
        return Vector2d[X, Y](self.y, self.x)

    def copy(self) -> Vector2d[X, Y]:
        return Vector2d[X, Y](self.x, self.y)

    def pivot_symmetry(self, symmetry: Symmetry) -> Vector2d[X, Y]:
        match symmetry:
            case Symmetry.ORIGIN:
                return Vector2d[X, Y](-self.x, -self.y)
            case Symmetry.X_AXIS:
                return Vector2d[X, Y](self.x, -self.y)
            case Symmetry.Y_AXIS:
                return Vector2d[X, Y](-self.x, self.y)


class IntVector2d(Vector2d[int, int]):
    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(x, y)

    def __eq__(self, other) -> bool:
        if not super().__eq__(other):
            return False
        return isinstance(other, IntVector2d)

    def __truediv__(self, other: Vector2d[X, Y]) -> Vector2d[X, Y]:
        if other.x == 0:
            raise ZeroDivisionError("The x of other vector is equal 0")
        if other.y == 0:
            raise ZeroDivisionError("The y of other vector is equal 0")

        return Vector2d[X, Y](int(self.x / other.x), int(self.y / other.y))

    def multiply_scalar(self, scalar: float) -> IntVector2d:
        return IntVector2d(int(self.x * scalar), int(self.y * scalar))


class BoardVector2d(IntVector2d):
    # override
    def __str__(self) -> str:
        return self.x_to_str() + self.y_to_str()

    def x_to_str(self) -> str:
        return chr(self.x + 97)

    def y_to_str(self) -> str:
        return str(self.y + 1)
