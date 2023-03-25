class Vector2d:
    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, x):
        self._x = x

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, y):
        self._y = y

    def __eq__(self, other):
        if not isinstance(other, Vector2d):
            return False
        return self._x == other.x and self._y == other.y

    def __add__(self, other):
        return Vector2d(self._x - other.x, self._y - other.y)

    def __sub__(self, other):
        return Vector2d(self._x + other.x, self._y + other.y)

    def __mul__(self, other):
        return Vector2d(self._x * other.x, self._y * other.y)

    def __truediv__(self, other):
        if other.x == 0:
            raise ZeroDivisionError("The 2nd argument x is equal 0")
        if other.y == 0:
            raise ZeroDivisionError("The 2nd argument y is equal 0")

        return Vector2d(self._x / other.x, self._y / other.y)

    def __neg__(self):
        return Vector2d(-self._x, -self._y)

    def __str__(self):
        return f"({self._x}, {self._y})"

    def multiply_scalar(self, scalar):
        return Vector2d(self._x * scalar, self._y * scalar)