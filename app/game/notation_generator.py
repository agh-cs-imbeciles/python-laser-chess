from game import Board
from game.piece.move.piece_move import PieceMove
from game.piece.move.piece_move_type import PieceMoveType
from game.piece import PieceModel
from game.observer import game_end_obs


class NotationGenerator:
    def __init__(self, board: Board):
        self._board = board
        self._ending_move = ""
        self._move_number = 0

    def __get_pieces(self, model: PieceModel, player_id: int):
        # self._board.
        pass

    def generate_last_move_string(self) -> str:
        self._move_number += 1
        lm = self._board.get_last_move()
        gen_str: str = ""

        if lm.move_type == PieceMoveType.DRAW or lm.move_type == PieceMoveType.QUEEN_SIDE_CASTLING \
                or lm.move_type == PieceMoveType.KING_SIDE_CASTLING:
            return str(lm.move_type)

        gen_str += str(lm.piece)

        if lm.piece.model == PieceModel.PAWN and lm.move_type == PieceMoveType.CAPTURE:
            gen_str += lm.origin.x_to_str()
        else:
            same_pieces = self._board.get_pieces_of(lm.piece.model, lm.piece.player_id)
            if len(same_pieces) > 1:
                pass

        if lm.move_type == PieceMoveType.CAPTURE:
            gen_str += str(lm)

        gen_str += lm.destination.x_to_str() + lm.destination.y_to_str()

        if lm.move_type == PieceMoveType.CHECK or lm.move_type == PieceMoveType.PROMOTION\
                or lm.move_type == PieceMoveType.CHECKMATE or lm.move_type == PieceMoveType.STALEMATE:
            gen_str += str(lm)

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
    def ending_move(self):
        return self._ending_move
