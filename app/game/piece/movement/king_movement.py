from __future__ import annotations
from typing import TYPE_CHECKING
from utils import BoardVector2d
from game.piece import Piece, PieceModel
from game.piece.movement import PieceMovement
from game.piece.move import PieceMoveType

if TYPE_CHECKING:
    from game import Board


class KingMovement(PieceMovement):
    def __init__(self, king: Piece, board: Board) -> None:
        super().__init__(king, board)
        self._initial_position: BoardVector2d = king.position.copy()

    def is_castling_legal(self, castling: PieceMoveType) -> bool:
        y: int = self._piece.position.y

        #
        # King-side castling
        #
        if castling == PieceMoveType.KING_SIDE_CASTLING:
            king_side_rook: Piece | None = self._board.get_piece(BoardVector2d(self._board.width - 1, y))
            vs = [self._piece.position + d for d in [BoardVector2d(1, 0), BoardVector2d(2, 0), BoardVector2d(0, 0)]]
            if (
                king_side_rook
                and king_side_rook.model == PieceModel.ROOK
                and not king_side_rook.moved()
            ):
                for pos in vs:
                    if self._board.is_check_at(self._piece.position, self._piece.player_id):
                        return False
                    if self._piece.position != pos and not self._board.can_move_to(pos, self._piece):
                        return False
                return True

        #
        # Queen-side castling
        #
        elif castling == PieceMoveType.QUEEN_SIDE_CASTLING:
            queen_side_rook: Piece | None = self._board.get_piece(BoardVector2d(0, y))
            vs = [self._piece.position + d for d in [BoardVector2d(-1, 0), BoardVector2d(-2, 0), BoardVector2d(0, 0)]]
            if (
                queen_side_rook
                and queen_side_rook.model == PieceModel.ROOK
                and not queen_side_rook.moved()
            ):
                for pos in vs:
                    if self._board.is_check_at(self._piece.position, self._piece.player_id):
                        return False
                    if self._piece.position != pos and not self._board.can_move_to(pos, self._piece):
                        return False
                return True

        return False

    # override
    def get_all_moves(self) -> list[list[BoardVector2d]]:
        p, b = self._get_aliases()
        moves = [[]]

        deltas = filter(lambda x: x != BoardVector2d(0, 0), [BoardVector2d(x, y) for y in range(-1, 2) for x in range(-1, 2)])
        for d in deltas:
            if not b.is_out_of_bounds(p.position + d):
                moves[0].append(p.position + d)

        return moves

    # override
    def get_legal_moves(self) -> list[list[BoardVector2d]]:
        # Clear legal moves
        self._legal_moves.clear()
        self._legal_moves.append([])

        # Aliases
        p, b = self._get_aliases()

        for m in self.get_all_moves()[0]:
            if b.can_move_to(m, p, capture=True):
                self._legal_moves[0].append(m)

        #
        # Castling
        #
        if not p.moved():
            #
            # King-side castling
            #
            if self.is_castling_legal(PieceMoveType.KING_SIDE_CASTLING):
                self._legal_moves[0].append(p.position + BoardVector2d(2, 0))
            #
            # Queen-side castling
            #
            if self.is_castling_legal(PieceMoveType.QUEEN_SIDE_CASTLING):
                self._legal_moves[0].append(p.position + BoardVector2d(-2, 0))

        return self._legal_moves
