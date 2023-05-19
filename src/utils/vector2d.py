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
        return Vector2d[X, Y](self.x * scalar, self.y * scalar)

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


class IntVector2d:
    def __init__(self, x: int, y: int):
        self._x: int = x
        self._y: int = y

    @property
    def x(self) -> int:
        return self._x

    @x.setter
    def x(self, x: int) -> None:
        self._x = x

    @property
    def y(self) -> int:
        return self._y

    @y.setter
    def y(self, y: int) -> None:
        self._y = y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __iter__(self) -> tuple[int, int]:
        return self.x, self.y

    def __eq__(self, other) -> bool:
        if not isinstance(other, IntVector2d):
            return False
        return self.x == other.x and self.y == other.y

    def __ne__(self, other) -> bool:
        return not self == other

    def __add__(self, other: IntVector2d) -> IntVector2d:
        return IntVector2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other: IntVector2d) -> IntVector2d:
        return IntVector2d(self.x - other.x, self.y - other.y)

    def __mul__(self, other: IntVector2d) -> IntVector2d:
        return IntVector2d(self.x * other.x, self.y * other.y)

    def __floordiv__(self, other: IntVector2d) -> IntVector2d:
        if other.x == 0:
            raise ZeroDivisionError("The x of other vector is equal 0")
        if other.y == 0:
            raise ZeroDivisionError("The y of other vector is equal 0")

        return IntVector2d(self.x // other.x, self.y // other.y)

    def __truediv__(self, other: IntVector2d) -> IntVector2d:
        if other.x == 0:
            raise ZeroDivisionError("The x of other vector is equal 0")
        if other.y == 0:
            raise ZeroDivisionError("The y of other vector is equal 0")

        return IntVector2d(int(self.x / other.x), int(self.y / other.y))

    def __neg__(self) -> IntVector2d:
        return IntVector2d(-self.x, -self.y)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def multiply_scalar(self, scalar: float) -> IntVector2d:
        return IntVector2d(int(self.x * scalar), int(self.y * scalar))

    def reverse_axis(self) -> IntVector2d:
        return IntVector2d(self.y, self.x)

    def copy(self) -> IntVector2d:
        return IntVector2d(self.x, self.y)

    def pivot_symmetry(self, symmetry: Symmetry) -> IntVector2d:
        match symmetry:
            case Symmetry.ORIGIN:
                return IntVector2d(-self.x, -self.y)
            case Symmetry.X_AXIS:
                return IntVector2d(self.x, -self.y)
            case Symmetry.Y_AXIS:
                return IntVector2d(-self.x, self.y)


class BoardVector2d(IntVector2d):
    @staticmethod
    def from_int_v2d(vector: IntVector2d) -> BoardVector2d:
        return BoardVector2d(vector.x, vector.y)

    @staticmethod
    def from_str(vector_str: str) -> BoardVector2d:
        if len(str) != 2:
            raise ValueError("Vector string is invalid [from_str()]")
        return BoardVector2d(ord(vector_str[0]) - 97, int(vector_str[1]) - 1)

    def x_to_str(self) -> str:
        return chr(self.x + 97)

    def y_to_str(self) -> str:
        return str(self.y + 1)

    # override
    def __str__(self) -> str:
        return self.x_to_str() + self.y_to_str()

    # override
    def __add__(self, other: IntVector2d) -> IntVector2d:
        return BoardVector2d.from_int_v2d(super().__add__(other))

    # override
    def __sub__(self, other: IntVector2d) -> IntVector2d:
        return BoardVector2d.from_int_v2d(super().__sub__(other))

    # override
    def __mul__(self, other: IntVector2d) -> IntVector2d:
        return BoardVector2d.from_int_v2d(super().__mul__(other))

    # override
    def __floordiv__(self, other: IntVector2d) -> IntVector2d:
        return BoardVector2d.from_int_v2d(super().__floordiv__(other))

    # override
    def __truediv__(self, other: IntVector2d) -> IntVector2d:
        return BoardVector2d.from_int_v2d(super().__truediv__(other))

    # override
    def __neg__(self) -> IntVector2d:
        return BoardVector2d.from_int_v2d(super().__neg__())

    # override
    def multiply_scalar(self, scalar: float) -> IntVector2d:
        return BoardVector2d.from_int_v2d(super().multiply_scalar(scalar))

    # override
    def reverse_axis(self) -> IntVector2d:
        return BoardVector2d.from_int_v2d(super().reverse_axis())

    # override
    def copy(self) -> IntVector2d:
        return BoardVector2d(self.x, self.y)

    # override
    def pivot_symmetry(self, symmetry: Symmetry) -> IntVector2d:
        return BoardVector2d.from_int_v2d(super().pivot_symmetry(symmetry))
