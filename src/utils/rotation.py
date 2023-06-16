from enum import Enum, unique, auto


@unique
class Rotation(Enum):
    CLOCKWISE       = auto()
    ANTICLOCKWISE   = auto()

    def __str__(self) -> str:
        match self:
            case Rotation.CLOCKWISE:
                return "cw"
            case Rotation.ANTICLOCKWISE:
                return "acw"
