from __future__ import annotations
from utils import BoardVector2d
import game.piece as pcs
from game.piece.move.piece_move_type import PieceMoveType


class PieceMove:
    def __init__(
        self,
        piece: pcs.Piece = None,
        origin: BoardVector2d = None,
        destination: BoardVector2d = None,
        promotion_piece: pcs.Piece | None = None,
        move_type: PieceMoveType = None
    ) -> None:
        if piece is None:
            self.move: int = None
        else:
            self.move: int = piece.player_id
        if move_type is None:
            self.move_types = []
        else:
            self.move_types = [move_type]

        self.piece: pcs.Piece = piece
        self.origin: BoardVector2d = origin
        self.destination: BoardVector2d = destination
        self.promotion_piece = promotion_piece

    def add_move_type(self, move_type: [PieceMoveType]) -> None:
        self.move_types.extend(move_type)

    def add_promotion_piece(self, promotion_piece: pcs.Piece) -> None:
        self.promotion_piece = promotion_piece

    def to_dict(self) -> dict[str, str | list[str]]:
        return {
            "piece": str(self.piece),
            "origin": str(self.origin),
            "destination": str(self.destination),
            "promotionPiece": str(self.promotion_piece),
            "move_types": [str(move_type) for move_type in self.move_types]
        }
