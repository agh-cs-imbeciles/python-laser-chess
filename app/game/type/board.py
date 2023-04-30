class File:
    def __init__(self, value: int) -> None:
        self._value = value

    def __str__(self) -> str:
        return str(self._value + 1)


class Rank:
    def __init__(self, value: int) -> None:
        self._value = value

    def __str__(self) -> str:
        return chr(self._value + 97)
