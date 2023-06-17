from __future__ import annotations
from typing import TYPE_CHECKING
from utils import BoardVector2d
from game.piece import PieceModel
from game.piece.movement import PieceMovement, PawnMovement, RangedPieceMovement

if TYPE_CHECKING:
    from game import Board
    from game.piece import Piece


class CheckManager:
    def __init__(self, board: Board) -> None:
        self._board = board
        self._checked_squares: list[dict[BoardVector2d, bool]] = [{}, {}]
        self._checking_pieces: list[dict[BoardVector2d, Piece]] = [{}, {}]
        self._critical_checked_squares: list[dict[BoardVector2d, bool]] = [{}, {}]
        self._pinned_pieces: list[dict[BoardVector2d, tuple[Piece, Piece]]] = [{}, {}]
        self._pinned_squares: list[dict[BoardVector2d, bool]] = [{}, {}]
        self._protected_pieces: list[dict[BoardVector2d, bool]] = [{}, {}]
        self._can_move: bool = True

    @property
    def checked_squares(self) -> list[dict[BoardVector2d, bool]]:
        return self._checked_squares

    @property
    def checking_pieces(self):
        return self._checking_pieces

    @checked_squares.setter
    def checked_squares(self, value: [dict[BoardVector2d, bool]]) -> None:
        self._checked_squares = value

    @property
    def pinned_pieces(self) -> list[dict[BoardVector2d, tuple[Piece, Piece]]]:
        return self._pinned_pieces

    def __filter_range_moves(self, moves: list[list[BoardVector2d]], color: int) -> list[list[BoardVector2d]]:
        for i, moves_row in enumerate(moves):
            for j, move in enumerate(moves_row):
                p = self._board.get_piece(move)
                if p and (p.model == PieceModel.KING and p.is_same_color(color) or p.model != PieceModel.KING):
                    moves[i] = moves_row[:j]
                    break

        return moves

    def __iterate_pin(self, piece: Piece, moves: list[list[BoardVector2d]]) -> tuple[list[BoardVector2d] | None, Piece | None] | None:
        b = self._board

        if len(moves) <= 1:
            return None, None

        for moves_row in moves:
            first_piece_idx = 0
            pieces: list[Piece] = []

            for i, move in enumerate(moves_row):
                if b.is_piece_at(move):
                    first_piece_idx = i
                    pieces.append(b.get_piece(move))
                if (
                        len(pieces) == 2
                        and pieces[1].model == PieceModel.KING
                        and not pieces[1].is_same_color(piece)
                        and pieces[0].is_same_color(pieces[1])
                ):
                    return moves_row[:first_piece_idx], pieces[0]

        return None, None

    def get_pinned_piece(self, piece: Piece, moves: list[list[BoardVector2d]]) -> Piece | None:
        _, p = self.__iterate_pin(piece, moves)
        return p

    def get_pinned_squares(self, piece: Piece, moves: list[list[BoardVector2d]]) -> list[BoardVector2d] | None:
        m, _ = self.__iterate_pin(piece, moves)
        return m

    def set_protecting_piece(self) -> None:
        b = self._board

        for piece, movement in b.pieces.values():
            moves = movement.get_capturable_moves()
            for moves_row in moves:
                pieces = list(
                    map(
                        lambda position: b.get_piece(position),
                        filter(lambda position: b.is_piece_at(position), moves_row)
                    )
                )
                if (
                    isinstance(movement, RangedPieceMovement)
                    and len(pieces) > 0
                    and pieces[0].is_same_color(piece)
                    and self._checking_pieces[pieces[0].player_id].get(pieces[0].position)
                ):
                    self._protected_pieces[pieces[0].player_id][pieces[0].position] = True
                elif not isinstance(movement, RangedPieceMovement):
                    for p in pieces:
                        if p.is_same_color(piece) and self._checking_pieces[p.player_id].get(p.position):
                            self._protected_pieces[p.player_id][p.position] = True

    def is_piece_protected(self, piece: Piece) -> bool:
        return self._protected_pieces[piece.player_id].get(piece.position, False)

    def is_check_at(self, position: BoardVector2d, player_id: int) -> bool:
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

    def is_king_dead(self, player_id: int) -> bool:
        return len(self._board.get_pieces_of(PieceModel.KING, player_id))==0


    def is_pinned_square(self, position: BoardVector2d, player_id: int) -> bool:
        return self._pinned_squares[player_id].get(position, False)

    def can_player_move(self, player_id: int) -> bool:
        #
        # Go through player's all pieces movement
        #
        pieces = self._board.get_player_piece_movements(player_id)
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

    def get_critical_square(self, position: BoardVector2d, player_id: int) -> bool | None:
        return self._critical_checked_squares[player_id].get(position)

    def update(self) -> None:
        for i in range(len(self._checked_squares)):
            self._checked_squares[i].clear()
            self._checking_pieces[i].clear()
            self._critical_checked_squares[i].clear()
            self._pinned_pieces[i].clear()
            self._pinned_squares[i].clear()
            self._protected_pieces[i].clear()

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
                for i, move in enumerate(moves_row):
                    for j, checked_squares in enumerate(self.checked_squares):
                        if piece.is_same_color(j): continue
                        p = self._board.get_piece(move)

                        # Check occurrence
                        if p and p.model == PieceModel.KING and not p.is_same_color(piece):
                            self._checking_pieces[piece.player_id][piece.position] = piece
                            if piece.model not in [PieceModel.PAWN, PieceModel.KNIGHT]:
                                self.add_critical_checked_squares(p.player_id, moves_row[:i])
                        checked_squares[move] = True

            pinned = self.get_pinned_piece(piece, moves)
            if pinned:
                self.pinned_pieces[pinned.player_id][pinned.position] = (pinned, piece)
                for sqr in self.get_pinned_squares(piece, moves):
                    self._pinned_squares[pinned.player_id][sqr] = True

        self._can_move = self.can_player_move((self._board.move_number + 1) % 2)
        self.set_protecting_piece()

    def add_critical_checked_squares(self, player_id: int, squares: list[BoardVector2d]) -> None:
        for s in squares:
            self._critical_checked_squares[player_id][s] = True
