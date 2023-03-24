class Vector2d:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Vector2d):
            return False
        return self.x == other.x and self.y == other.y

    def __add__(self, other):
        return Vector2d(self.x - other.x, self.y - other.y)

    def __sub__(self, other):
        return Vector2d(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Vector2d(self.x * other.x, self.y * other.y)

    def __truediv__(self, other):
        if other.x == 0:
            raise ZeroDivisionError("The 2nd argument x is equal 0")
        if other.y == 0:
            raise ZeroDivisionError("The 2nd argument y is equal 0")

        return Vector2d(self.x / other.x, self.y / other.y)

    def __neg__(self):
        return Vector2d(-self.x, -self.y)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def multiply_scalar(self, scalar):
        return Vector2d(self.x * scalar, self.y * scalar)