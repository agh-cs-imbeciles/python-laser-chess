from enum import Enum


class GameEnding(Enum):
    CHECKMATE   = 1
    STALEMATE   = 2
    LASER_MATE  = 3
    DRAW        = 4
    TIME_END    = 5
