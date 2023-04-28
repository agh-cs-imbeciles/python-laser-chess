from enum import Enum


class PieceMoveType(Enum):
    MOVE                = 0
    CAPTURE             = 1
    KING_SIDE_CASTLING  = 2
    QUEEN_SIDE_CASTLING = 3
    PROMOTION           = 4
    CHECK               = 5
    CHECKMATE           = 6
    STALEMATE           = 7
    DRAW                = 8
