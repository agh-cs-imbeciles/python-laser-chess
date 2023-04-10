from __future__ import annotations
from typing import TYPE_CHECKING
from game.piece.move import PieceMoveType

if TYPE_CHECKING:
    from game import Board
    from game.piece import Piece


class PieceMoveDetector:
    @staticmethod
    def detect(board: Board, moved_piece: Piece, other_piece: Piece | None) -> PieceMoveType:
        #
        # Capture
        #
        if other_piece is not None:
            return PieceMoveType.CAPTURE
        #
        # Mate
        #
        if False:
            return PieceMoveType.CHECKMATE
        #
        # Stalemate
        #
        if False:
            return PieceMoveType.STALEMATE
        #
        # Check
        #
        if board.is_king_under_check(moved_piece.player_id):
            return PieceMoveType.CHECK
        #
        # Castling
        #
        if False:
            pass
        return PieceMoveType.MOVE
