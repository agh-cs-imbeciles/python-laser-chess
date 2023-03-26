from enum import Enum


class PieceMoveType(Enum):
    MOVE        = 0
    CAPTURE     = 1
    CASTLING    = 2
    CHECK       = 3
    CHECKMATE   = 4