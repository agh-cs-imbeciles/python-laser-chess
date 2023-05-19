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
    ROTATION            = 9

    def __str__(self):
        match self.value:
            case PieceMoveType.DRAW.value:
                return "="
            case PieceMoveType.QUEEN_SIDE_CASTLING.value:
                return "O-O-O"
            case PieceMoveType.KING_SIDE_CASTLING.value:
                return "O-O"
            case PieceMoveType.MOVE.value:
                return ""
            case PieceMoveType.STALEMATE.value:
                return "$"
            case PieceMoveType.CHECKMATE.value:
                return "#"
            case PieceMoveType.CHECK.value:
                return "+"
            case PieceMoveType.CAPTURE.value:
                return "x"
            case PieceMoveType.PROMOTION.value:
                return "="
