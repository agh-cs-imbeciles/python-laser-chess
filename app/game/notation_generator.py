from game import Board
from game.piece.move.piece_move import PieceMove
from game.piece.move.piece_move_type import PieceMoveType
from game.piece import PieceModel


class NotationGenerator:
    def __init__(self, board: Board):
        self._board = board
        self._move_number = 0
        # self._moves_list = moves_list

    def __get_pieces(self, model: PieceModel, player_id: int):
        # self._board.
        pass
    def generate_last_move_string(self) -> str:
        lm = self._board.get_last_move()
        gen_str: str = ""
        match lm.move_type:
            case PieceMoveType.DRAW:
                return "="
            case PieceMoveType.QUEEN_SIDE_CASTLING:
                return "O-O-O"
            case PieceMoveType.KING_SIDE_CASTLING:
                return "O-O"
        gen_str += lm.piece.model
        if lm.piece.model == PieceModel.PAWN:
            gen_str += str(lm.origin)[0]
        # else:



    def generate_ending_string(self):
        pass
