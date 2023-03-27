from enum import Enum


class PieceMoveType(Enum):
    MOVE        = 0
    CAPTURE     = 1
    CASTLING    = 2
    PROMOTION   = 3
    CHECK       = 4
    CHECKMATE   = 5
