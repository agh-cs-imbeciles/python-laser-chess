from typing import Tuple, Any
from game.board import Board
from game.pieces.piece import Piece
from game.pieces.piece_model import PieceModel
from utils.vector2d import Vector2d
from game.pieces.move.piece_move import PieceMove


class Game:
    def __init__(self) -> None:
        self.__BOARD_SIZE: int = 8
        self._board: Board = Board(self.__BOARD_SIZE, self.__BOARD_SIZE)
        self._players: list[int] = []
        self._moves_history: list[Tuple[PieceMove, PieceMove]] = []

        self.__init_board()
        # self.move_piece()
        
    @property
    def board(self) -> Board:
        return self._board

    @property
    def players(self) -> list[Any]:
        return self._players

    @players.setter
    def players(self, value: list[Any]) -> None:
        self._players = value

    @property
    def moves_history(self) -> list[Any]:
        return self._moves_history

    def __init_board(self) -> None:
        pawn_xs = [2, 3, 4, 5]
        for x in pawn_xs:
            self.board.add_pieces([
                Piece(PieceModel.PAWN, Vector2d(x, 1), 0),
                Piece(PieceModel.PAWN, Vector2d(x, self.__BOARD_SIZE - 2), 1)]
            )
        self.board.add_pieces([
            Piece(PieceModel.PAWN, Vector2d(0, 1), 0),
            Piece(PieceModel.PAWN, Vector2d(self.__BOARD_SIZE - 1, self.__BOARD_SIZE - 2), 1)
        ])

    def move_piece(self, piece: Piece, to: Vector2d):
        piece.move(to)
