from __future__ import annotations
from enum import Enum
from utils.vector2d import BoardVector2d


class MirrorDirections(Enum):
    UPPER_LEFT   = 0
    UPPER_RIGHT  = 1
    BOTTOM_RIGHT = 2
    BOTTOM_LEFT  = 3

    def to_vector(self) -> BoardVector2d:
        match self:
            case MirrorDirections.UPPER_LEFT:
                return BoardVector2d(-1, 1)
            case MirrorDirections.UPPER_RIGHT:
                return BoardVector2d(1, 1)
            case MirrorDirections.BOTTOM_LEFT:
                return BoardVector2d(-1, -1)
            case MirrorDirections.BOTTOM_RIGHT:
                return BoardVector2d(1, -1)

    def left(self) -> MirrorDirections:
        return MirrorDirections((self.value-1) % 4)

    def right(self) -> MirrorDirections:
        return MirrorDirections((self.value+1) % 4)


