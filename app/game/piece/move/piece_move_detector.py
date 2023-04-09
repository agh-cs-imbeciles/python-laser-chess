from __future__ import annotations
from typing import TYPE_CHECKING
from utils import Vector2d

if TYPE_CHECKING:
    from game import Board
    from game.piece import Piece
    from game.piece.move import PieceMoveType


class PieceMoveDetector:
    @staticmethod
    def detect(board: Board, piece: Piece, origin: Vector2d, destination: Vector2d) -> PieceMoveType:
        if board.is_piece_at(destination) and piece.player_id == board.get_piece(destination).player_id:
            return PieceMoveType.CAPTURE
        return PieceMoveType.MOVE
