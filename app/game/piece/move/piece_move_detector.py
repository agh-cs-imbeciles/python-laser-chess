from __future__ import annotations
from typing import TYPE_CHECKING
from utils import Vector2d
from game.piece import PieceModel
from game.piece.move import PieceMoveType

if TYPE_CHECKING:
    from game import Board
    from game.piece import Piece


class PieceMoveDetector:
    @staticmethod
    def detect(board: Board, moved_piece: Piece, other_piece: Piece | None, destination: Vector2d) -> PieceMoveType:
        #
        # Capture
        #
        if other_piece is not None:
            # TODO: Pawns
            return PieceMoveType.CAPTURE
        #
        # Mate and Stalemate
        #
        player_move = board.get_ending_move()
        if player_move is not None:
            return player_move
        #
        # Check
        #
        if board.is_king_under_check((moved_piece.player_id + 1) % 2):
            return PieceMoveType.CHECK
        #
        # Castling
        #
        if moved_piece.model == PieceModel.KING and board.last_move[0] and abs((destination - board.last_move[1]).x) == 2:
            dx = (destination - board.last_move[1]).x
            castling = PieceMoveType.KING_SIDE_CASTLING if dx > 0 else PieceMoveType.QUEEN_SIDE_CASTLING

            rook_pos = Vector2d(
                board.width - 1 if castling == PieceMoveType.KING_SIDE_CASTLING else 0,
                moved_piece.position.y
            )
            if not board.is_piece_at(rook_pos) or board.get_piece(rook_pos).model != PieceModel.ROOK:
                raise ValueError("Castling is not allowed")

            return castling

        return PieceMoveType.MOVE
