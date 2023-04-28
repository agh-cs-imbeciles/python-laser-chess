from enum import Enum


class PieceMoveType(Enum):
    MOVE                = 0
    CAPTURE             = 1
    # CASTLING            = 2
    KING_SIDE_CASTLING  = 3
    QUEEN_SIDE_CASTLING = 4
    PROMOTION           = 5
    CHECK               = 6
    CHECKMATE           = 7
    STALEMATE           = 8
    DRAW                = 9
