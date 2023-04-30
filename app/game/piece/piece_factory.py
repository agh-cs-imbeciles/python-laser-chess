from __future__ import annotations
from typing import TYPE_CHECKING
from utils import BoardVector2d
from game.piece import Piece, PieceModel
from game.piece.movement import PieceMovement, \
                                KingMovement, \
                                QueenMovement, \
                                PawnMovement, \
                                BishopMovement, \
                                RookMovement, \
                                KnightMovement

if TYPE_CHECKING:
    from game import Board


class PieceFactory:
    def __init__(self, board: Board):
        self._board = board

    def create_piece(self, piece_model: PieceModel, position: BoardVector2d, color: int) -> tuple[Piece, PieceMovement]:
        match piece_model:
            case PieceModel.KING:
                p = Piece(PieceModel.KING, position, color)
                return p, KingMovement(p, self._board)
            case PieceModel.QUEEN:
                p = Piece(PieceModel.QUEEN, position, color)
                return p, QueenMovement(p, self._board)
            case PieceModel.PAWN:
                p = Piece(PieceModel.PAWN, position, color)
                dir = BoardVector2d(0, 1) if color == 0 else BoardVector2d(0, -1)
                enp = BoardVector2d(position.x, self._board.height - 4) if color == 0 else BoardVector2d(position.x, 3)
                pro = BoardVector2d(position.x, self._board.height - 1) if color == 0 else BoardVector2d(position.x, 0)
                return p, PawnMovement(p, self._board, dir, enp, pro)
            case PieceModel.BISHOP:
                p = Piece(PieceModel.BISHOP, position, color)
                return p, BishopMovement(p, self._board)
            case PieceModel.ROOK:
                p = Piece(PieceModel.ROOK, position, color)
                return p, RookMovement(p, self._board)
            case PieceModel.KNIGHT:
                p = Piece(PieceModel.KNIGHT, position, color)
                return p, KnightMovement(p, self._board)
