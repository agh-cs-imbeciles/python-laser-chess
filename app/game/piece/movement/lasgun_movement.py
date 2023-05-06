from __future__ import annotations
from typing import TYPE_CHECKING
from game.piece import Piece
from game.piece.movement import PieceMovement
from utils import BoardVector2d


if TYPE_CHECKING:
    from game import Board

class LasgunMovement(PieceMovement):
    def __init__(self, bishop: Piece, board: Board) -> None:
        super().__init__(bishop, board)

    def get_all_moves(self) -> list[list[BoardVector2d]]:
        return []

    def get_legal_moves(self) -> list[list[BoardVector2d]]:
        return []
