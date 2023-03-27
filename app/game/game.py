from typing import Tuple, Any
from utils import Vector2d
from game import Board
from game.pieces import Piece, PieceModel
from game.pieces.move import PieceMove
from game.pieces.movement import KingMovement,\
                                 QueenMovement,\
                                 PawnMovement,\
                                 BishopMovement,\
                                 RookMovement,\
                                 KnightMovement


class Game:
    def __init__(self) -> None:
        self.__BOARD_SIZE: int = 8
        self._board: Board = Board(self.__BOARD_SIZE, self.__BOARD_SIZE)
        self._players: list[int] = []
        self._moves_history: list[Tuple[PieceMove, PieceMove]] = []

        self.__init_board()

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
        # Kings
        self.__init_kings()
        # Queens
        self.__init_hetmanice()
        # Pawns
        self.__init_pawns()
        # Bishops 2137
        self.__init_bishops()
        # Rooks
        self.__init_rooks()
        # Knights
        self.__init_knights()

    def __init_kings(self):
        king_data = [
            (Vector2d(4, 0), 0),
            (Vector2d(4, self.board.height - 1), 1),
        ]
        for kd in king_data:
            p = Piece(PieceModel.KING, kd[0], kd[1])
            self.board.add_piece((p, KingMovement(p, self.board)))

    def __init_hetmanice(self):
        queen_data = [
            (Vector2d(3, 0), 0),
            (Vector2d(3, self.board.height - 1), 1),
        ]
        for qd in queen_data:
            p = Piece(PieceModel.QUEEN, qd[0], qd[1])
            self.board.add_piece((p, QueenMovement(p, self.board)))

    def __init_pawns(self):
        pawn_xs = [2, 3, 4, 5]
        for x in pawn_xs:
            p1 = Piece(PieceModel.PAWN, Vector2d(x, 1), 0)
            p2 = Piece(PieceModel.PAWN, Vector2d(x, self.__BOARD_SIZE - 2), 1)
            self.board.add_pieces([
                (p1, PawnMovement(p1, self.board, Vector2d(0, 1), Vector2d(0, 4), Vector2d(0, 7))),
                (p2, PawnMovement(p2, self.board, Vector2d(0, -1), Vector2d(0, 3), Vector2d(0, 0))),
            ])
        p1 = Piece(PieceModel.PAWN, Vector2d(0, 1), 0)
        p2 = Piece(PieceModel.PAWN, Vector2d(self.__BOARD_SIZE - 1, self.__BOARD_SIZE - 2), 1)
        self.board.add_pieces([
            (p1, PawnMovement(p1, self.board, Vector2d(0, 1), Vector2d(0, 4), Vector2d(0, 7))),
            (p2, PawnMovement(p2, self.board, Vector2d(0, -1), Vector2d(0, 3), Vector2d(0, 0)))
        ])

    def __init_bishops(self):
        bishop_data = [
            (Vector2d(2, 0), 0), (Vector2d(5, 0), 0),
            (Vector2d(2, self.board.height - 1), 1), (Vector2d(5, self.board.height - 1), 1),
        ]
        for bd in bishop_data:
            p = Piece(PieceModel.BISHOP, bd[0], bd[1])
            self.board.add_piece((p, BishopMovement(p, self.board)))

    def __init_rooks(self):
        rook_data = [
            (Vector2d(0, 0), 0), (Vector2d(7, 0), 0),
            (Vector2d(0, self.board.height - 1), 1), (Vector2d(7, self.board.height - 1), 1),
        ]
        for rd in rook_data:
            p = Piece(PieceModel.ROOK, rd[0], rd[1])
            self.board.add_piece((p, RookMovement(p, self.board)))

    def __init_knights(self):
        knight_data = [
            (Vector2d(1, 0), 0), (Vector2d(6, 0), 0),
            (Vector2d(1, self.board.height - 1), 1), (Vector2d(6, self.board.height - 1), 1),
        ]
        for kd in knight_data:
            p = Piece(PieceModel.KNIGHT, kd[0], kd[1])
            self.board.add_piece((p, KnightMovement(p, self.board)))

    def move_piece(self, piece: Piece, destination: Vector2d):
        if self.board.move_number != piece.player_id:
            return

        piece_movement = self.board.get_piece_movement(piece.position)
        legal = piece_movement.get_legal_moves()
        if destination in legal:
            piece.move(destination)
            self.board.move_number = (self.board.move_number + 1) % 2
