from __future__ import annotations
from typing import TYPE_CHECKING
from utils import Vector2d
from game.piece import PieceModel
from game.piece.movement import PieceMovement, PawnMovement

if TYPE_CHECKING:
    from game import Board
    from game.piece import Piece


class CheckManager:
    def __init__(self, board: Board) -> None:
        self._board = board
        self._checked_squares: list[dict[Vector2d, bool]] = [{}, {}]
        self._checking_pieces: list[dict[Vector2d, tuple[Piece, PieceMovement]]] = [{}, {}]
        self._critical_checked_squares: list[dict[Vector2d, bool]] = [{}, {}]
        self._pinned_pieces: list[dict[Vector2d, Piece]] = [{}, {}]

    @property
    def checked_squares(self) -> list[dict[Vector2d, bool]]:
        return self._checked_squares

    @checked_squares.setter
    def checked_squares(self, value: [dict[Vector2d, bool]]) -> None:
        self._checked_squares = value
        
    @property
    def pinned_pieces(self) -> list[dict[Vector2d, Piece]]:
        return self._pinned_pieces
    
    @pinned_pieces.setter
    def pinned_pieces(self, value) -> None:
        self._pinned_pieces = value

    def is_check_at(self, position: Vector2d, player_id: int) -> bool:
        return self._checked_squares[player_id].get(position) is not None

    def is_king_under_check(self, player_id: int) -> bool:
        if not 0 <= player_id < len(self._board.kings):
            raise ValueError("Invalid player id")
        return self._checked_squares[player_id].get(self._board.kings[player_id].position) is not None

    def get_critical_square(self, position: Vector2d, player_id: int) -> bool | None:
        return self._critical_checked_squares[player_id].get(position)

    def update(self) -> None:
        for i in range(len(self._checked_squares)):
            self._checked_squares[i].clear()
        for player_sqrs in self._critical_checked_squares:
            player_sqrs.clear()
        for pieces in self.pinned_pieces:
            pieces.clear()

        for key, piece_data in self._board.pieces.items():
            #
            # Pawn capture moves
            #
            if isinstance(piece_data[1], PawnMovement):
                pos: Vector2d = piece_data[0].position + piece_data[1].direction
                for i, checked_squares in enumerate(self.checked_squares):
                    if piece_data[0].player_id == i: continue
                    checked_squares[pos + Vector2d(-1, 0)] = True
                    checked_squares[pos + Vector2d(1, 0)] = True
                continue

            #
            # Other pieces moves
            #
            for moves in piece_data[1].get_legal_moves():
                for move in moves:
                    for i, checked_squares in enumerate(self.checked_squares):
                        if piece_data[0].player_id == i: continue
                        p = self._board.get_piece(move)
                        if p is not None and p.model == PieceModel.KING and p.player_id != piece_data[0].player_id:
                            # self._checking_pieces[p.player_id][move] = piece_data
                            if piece_data[0].model != PieceModel.PAWN and piece_data[0].model != PieceModel.KNIGHT:
                                self.add_critical_checked_squares(p.player_id, moves)
                        checked_squares[move] = True

            pinned = piece_data[1].get_pinned_piece()
            if pinned:
                self.pinned_pieces[pinned.player_id][pinned.position] = pinned

    def add_critical_checked_squares(self, player_id: int, squares: list[Vector2d]):
        for s in squares:
            self._critical_checked_squares[player_id][s] = True
