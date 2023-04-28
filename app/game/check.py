from __future__ import annotations
from typing import TYPE_CHECKING
from utils import Vector2d
from game.piece import PieceModel
from game.piece.movement import PieceMovement, PawnMovement, RangedPieceMovement

if TYPE_CHECKING:
    from game import Board
    from game.piece import Piece


class CheckManager:
    def __init__(self, board: Board) -> None:
        self._board = board
        self._checked_squares: list[dict[Vector2d, bool]] = [{}, {}]
        self._checking_pieces: list[dict[Vector2d, Piece]] = [{}, {}]
        self._critical_checked_squares: list[dict[Vector2d, bool]] = [{}, {}]
        self._pinned_pieces: list[dict[Vector2d, tuple[Piece, Piece]]] = [{}, {}]
        self._can_move: bool = True

    @property
    def checked_squares(self) -> list[dict[Vector2d, bool]]:
        return self._checked_squares

    @property
    def checking_pieces(self):
        return self._checking_pieces

    @checked_squares.setter
    def checked_squares(self, value: [dict[Vector2d, bool]]) -> None:
        self._checked_squares = value

    @property
    def pinned_pieces(self) -> list[dict[Vector2d, tuple[Piece, Piece]]]:
        return self._pinned_pieces

    def __filter_range_moves(self, moves: list[list[Vector2d]], color: int) -> list[list[Vector2d]]:
        for i, moves_row in enumerate(moves):
            for j, move in enumerate(moves_row):
                p = self._board.get_piece(move)
                if p and (p.model == PieceModel.KING and p.is_same_color(color) or p.model != PieceModel.KING):
                    # if not p.is_same_color(color):
                    #     moves[i] = moves_row[:j + 1]
                    # else:
                    #     moves[i] = moves_row[:j]
                    moves[i] = moves_row[:j]
                    break

        return moves

    def get_pinned_piece(self, piece: Piece, piece_movement: PieceMovement) -> Piece | None:
        moves = piece_movement.get_all_moves()
        b = self._board

        if len(moves) <= 1:
            return None

        for moves_row in moves:
            for move in moves_row:
                p = b.get_piece(move)
                if p and p.model == PieceModel.KING and not p.is_same_color(piece):
                    return p

        return None

    def is_check_at(self, position: Vector2d, player_id: int) -> bool:
        return self._checked_squares[player_id].get(position) is not None

    def is_king_under_check(self, player_id: int) -> bool:
        if not 0 <= player_id < len(self._board.kings):
            raise ValueError("Invalid player id")
        return self._checked_squares[player_id].get(self._board.kings[player_id].position) is not None

    def is_checkmate(self, player_id: int) -> bool:
        if self._can_move:
            return False
        return self.is_king_under_check(player_id)

    def is_stalemate(self, player_id: int) -> bool:
        if self._can_move:
            return False
        return not self.is_king_under_check(player_id)

    def can_player_move(self, player_id: int) -> bool:
        #
        # Go through player's all pieces movement
        #
        pieces = self._board.get_player_pieces_movements(player_id)
        for pie, mov in pieces:
            ll = mov.get_legal_moves()
            all_moves = []
            for l in ll:
                all_moves.extend(l)
            #
            # If there are possible movements then it is not a stalemate
            #
            if len(all_moves) != 0:
                return True
        return False

    def get_critical_square(self, position: Vector2d, player_id: int) -> bool | None:
        return self._critical_checked_squares[player_id].get(position)

    def update(self) -> None:
        for i in range(len(self._checked_squares)):
            self._checked_squares[i].clear()
            self._checking_pieces[i].clear()
            self._critical_checked_squares[i].clear()
            self._pinned_pieces[i].clear()

        for key, piece_data in self._board.pieces.items():
            piece, movement = piece_data

            #
            # Pawn capture moves
            #
            if isinstance(movement, PawnMovement):
                for i, checked_squares in enumerate(self.checked_squares):
                    if piece.is_same_color(i): continue
                    for capture_position in movement.get_capturable_moves()[0]:
                        if self._board.can_move_to(capture_position, piece, capture_required=True):
                            checked_squares[capture_position] = True
                continue

            #
            # Other pieces moves
            #
            moves = self.__filter_range_moves(movement.get_all_moves(), piece.player_id) \
                if isinstance(movement, RangedPieceMovement) \
                else movement.get_legal_moves()
            for moves_row in moves:
                for move in moves_row:
                    for i, checked_squares in enumerate(self.checked_squares):
                        if piece.is_same_color(i): continue
                        p = self._board.get_piece(move)

                        # Check occurrence
                        if p and p.model == PieceModel.KING and not p.is_same_color(piece):
                            self._checking_pieces[piece.player_id][piece.position] = piece
                            if piece.model != PieceModel.PAWN and piece.model != PieceModel.KNIGHT:
                                self.add_critical_checked_squares(p.player_id, moves_row)
                        checked_squares[move] = True

                pinned = self.get_pinned_piece(piece, movement)
                if pinned:
                    self.pinned_pieces[pinned.player_id][pinned.position] = (pinned, piece)

        self._can_move = self.can_player_move((self._board.move_number + 1) % 2)

    def add_critical_checked_squares(self, player_id: int, squares: list[Vector2d]) -> None:
        for s in squares:
            self._critical_checked_squares[player_id][s] = True
