class Vector2d:
    def __init__(self, x: float = 0, y: float = 0):
        self._x: float = x
        self._y: float = y

    @property
    def x(self) -> float:
        return self._x

    @x.setter
    def x(self, x) -> None:
        self._x = x

    @property
    def y(self) -> float:
        return self._y

    @y.setter
    def y(self, y) -> None:
        self._y = y

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __eq__(self, other) -> bool:
        if not isinstance(other, Vector2d):
            return False
        return self.x == other.x and self.y == other.y

    def __add__(self, other: "Vector2d") -> "Vector2d":
        return Vector2d(self.x - other.x, self.y - other.y)

    def __sub__(self, other: "Vector2d") -> "Vector2d":
        return Vector2d(self.x + other.x, self.y + other.y)

    def __mul__(self, other: "Vector2d") -> "Vector2d":
        return Vector2d(self.x * other.x, self.y * other.y)

    def __truediv__(self, other: "Vector2d") -> "Vector2d":
        if other.x == 0:
            raise ZeroDivisionError("The 2nd argument x is equal 0")
        if other.y == 0:
            raise ZeroDivisionError("The 2nd argument y is equal 0")

        return Vector2d(self.x / other.x, self.y / other.y)

    def __neg__(self) -> "Vector2d":
        return Vector2d(-self.x, -self.y)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"

    def multiply_scalar(self, scalar: float) -> "Vector2d":
        return Vector2d(self.x * scalar, self.y * scalar)

    def reverse_axis(self) -> "Vector2d":
        return Vector2d(self.y, self.y)

    def copy(self) -> "Vector2d":
        return Vector2d(self.x, self.y)
