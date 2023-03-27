from utils import Vector2d
import game as g
import game.pieces as pcs
import game.pieces.movement as mvm


class QueenMovement(mvm.BishopMovement, mvm.RookMovement):
    def __init__(self, pawn: pcs.Piece, board: g.Board) -> None:
        super().__init__(pawn, board)

    def get_legal_moves(self) -> list[Vector2d]:
        super().get_legal_moves()
        return self._legal_moves
