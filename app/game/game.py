from typing import Tuple, Any
from utils import Vector2d
from game import Board
from game.pieces import Piece, PieceModel
from game.pieces.move import PieceMove
from game.pieces.movement import PawnMovement


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
            p1 = Piece(PieceModel.PAWN, Vector2d(x, 1), 0)
            p2 = Piece(PieceModel.PAWN, Vector2d(x, self.__BOARD_SIZE - 2), 1)
            self.board.add_pieces([
                (p1, PawnMovement(p1, self.board, Vector2d(0, -1), Vector2d(0, 4), Vector2d(0, 7))),
                (p2, PawnMovement(p2, self.board, Vector2d(0, 1), Vector2d(0, 3), Vector2d(0, 0)))
            ])
        p1 = Piece(PieceModel.PAWN, Vector2d(0, 1), 0)
        p2 = Piece(PieceModel.PAWN, Vector2d(self.__BOARD_SIZE - 1, self.__BOARD_SIZE - 2), 1)
        self.board.add_pieces([
            (p1, PawnMovement(p1, self.board, Vector2d(0, -1), Vector2d(0, 4), Vector2d(0, 7))),
            (p2, PawnMovement(p2, self.board, Vector2d(0, 1), Vector2d(0, 3), Vector2d(0, 0)))
        ])

    def move_piece(self, piece: Piece, to: Vector2d):
        piece.move(to)
