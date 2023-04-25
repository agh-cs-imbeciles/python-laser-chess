from __future__ import annotations
from typing import TYPE_CHECKING

from utils import Vector2d
from game.piece.piece_model import PieceModel
from game.piece.piece import Piece
from game.piece.movement.pawn_movement import PawnMovement
from game.piece.movement.movement import Movement
from game.piece.piece_factory import PieceFactory

if TYPE_CHECKING:
    from game.board import Board

class PromotionManager:
    def __init__(self, board: Board):
        self._board: Board = board
        self._factory: PieceFactory = PieceFactory(board)
        self._to_promote: Piece | None = None
        self._possible_types = [PieceModel.ROOK, PieceModel.QUEEN, PieceModel.KNIGHT, PieceModel.BISHOP]
    def check_promotion(self,piece: Piece):
        if piece.model == PieceModel.PAWN:
            position = piece.position
            piece_movement: PawnMovement = self._board.get_piece_movement(position)
            if piece_movement.promotion_position.y == piece.position.y:
                self._to_promote = piece
    def is_promotion_possible(self):
        return self._to_promote is not None
    def get_promotion_piece(self)-> Piece | None:
        return self._to_promote
    def try_to_promote(self, model: PieceModel) -> tuple[Piece, Movement] | None:
        if model not in self._possible_types or self._to_promote is None:
            return
        new_piece = self._factory.create_piece(model, self._to_promote.position, self._to_promote.player_id)
        self._board.destroy_piece(self._to_promote)
        self._to_promote = None
        return new_piece
    def get_possible_types(self):
        return self._possible_types
