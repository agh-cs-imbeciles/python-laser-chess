from __future__ import annotations

from game import Board
from game.piece.move.piece_move import PieceMove
from game.piece.move.piece_move_type import PieceMoveType
from game.piece import PieceModel
from game.observer import game_end_obs
from game.ambiguous_enum import AmbiguousNotation


class NotationGenerator(object):
    def __init__(self, board: Board):
        self._ambiguity = AmbiguousNotation.NONE
        self._board = board
        self._ending_move = ""
        self._move_number = 0

    def generate_last_move_string(self) -> str:
        self._move_number += 1
        lm = self._board.get_last_move()
        gen_str: str = ""
        for m in lm.move_types:
            if m == PieceMoveType.DRAW or m == PieceMoveType.QUEEN_SIDE_CASTLING \
                    or m == PieceMoveType.KING_SIDE_CASTLING:
                return str(m)
        gen_str += str(lm.piece)
        if lm.piece.model == PieceModel.PAWN and PieceMoveType.CAPTURE in lm.move_types:
            gen_str += lm.origin.x_to_str()
        else:
            same_pieces = self._board.get_pieces_of(lm.piece.model, lm.piece.player_id)
            match self._ambiguity:
                case AmbiguousNotation.FILE:
                    gen_str += lm.origin.y_to_str()
                case AmbiguousNotation.RANK:
                    gen_str += lm.origin.x_to_str()
                case AmbiguousNotation.BOTH:
                    gen_str += lm.origin.y_to_str() + lm.origin.x_to_str()
        if PieceMoveType.CAPTURE in lm.move_types:
            gen_str += str(PieceMoveType.CAPTURE)
        gen_str += lm.destination.x_to_str() + lm.destination.y_to_str()
        if PieceMoveType.PROMOTION in lm.move_types:
            gen_str += str(PieceMoveType.PROMOTION) + str(lm.promotion_piece)
        for m in lm.move_types:
            if m == PieceMoveType.CHECK or m == PieceMoveType.CHECKMATE or m == PieceMoveType.STALEMATE:
                gen_str += str(m)
        return gen_str

    # override
    def on_end(self, winner: int, typed: PieceMoveType):
        if typed is None:
            self._ending_move = ""
            return
        if typed == PieceMoveType.STALEMATE or typed == PieceMoveType.DRAW:
            self._ending_move = "½-½"
            return
        if winner == 0:
            self._ending_move = "1-0"
        else:
            self._ending_move = "0-1"

    @property
    def ambiguity(self):
        return self._ambiguity

    @ambiguity.setter
    def ambiguity(self, ambig: AmbiguousNotation) -> None:
        self._ambiguity = ambig

    @property
    def ending_move(self):
        return self._ending_move
