from typing import Tuple, Any
from utils import Vector2d
from game import Board
from game.piece import Piece, PieceModel, PieceFactory
from game.piece.move import PieceMove, PieceMoveType, PieceMoveDetector
from game.piece.movement import PieceMovement
from game.observer.game_end_obs import GameEndObserver


class Game:
    def __init__(self) -> None:
        self.__BOARD_SIZE: int = 8
        self._board: Board = Board(self, self.__BOARD_SIZE, self.__BOARD_SIZE)
        self._players: list[int] = []
        self._moves_history: list[Tuple[PieceMove, PieceMove]] = []
        self._piece_factory = PieceFactory(self._board)
        self._observers: list[GameEndObserver] = []
        self.__init_board()

    # override
    def on_position_change(self, piece: Piece, move_type: PieceMoveType) -> None:
        # print(move_type)

        if move_type == PieceMoveType.KING_SIDE_CASTLING:
            self.move_piece(
                self._board.get_piece(Vector2d(self.__BOARD_SIZE - 1, piece.position.y)),
                piece.position + Vector2d(-1, 0)
            )
        elif move_type == PieceMoveType.QUEEN_SIDE_CASTLING:
            self.move_piece(
                self._board.get_piece(Vector2d(0, piece.position.y)),
                piece.position + Vector2d(1, 0)
            )
        self.end_if_conditions_fulfiled()
        pass

    def end_if_conditions_fulfiled(self) -> None:
        mov = self._board.get_ending_move()
        if mov is not None:
            for obs in self._observers:
                obs.on_end(self._board.move_number, mov)

    def add_observer(self,observer: GameEndObserver):
        self._observers.append(observer)

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

    def __add_piece(self, piece_data: tuple[Piece, PieceMovement]):
        # piece_data[0].add_observer(self)
        self.board.add_piece(piece_data)

    def __init_board(self) -> None:
        # Kings
        self.__init_kings()
        # Queens
        self.__init_hetmanice()
        # Pawns
        self.__init_pawns()
        # Bishops 2137 666
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
        for pos, color in king_data:
            self.__add_piece(self._piece_factory.create_piece(PieceModel.KING, pos, color))

    def __init_hetmanice(self):
        queen_data = [
            (Vector2d(3, 0), 0),
            (Vector2d(3, self.board.height - 1), 1),
        ]
        for pos, color in queen_data:
            self.__add_piece(self._piece_factory.create_piece(PieceModel.QUEEN, pos, color))

    def __init_pawns(self):
        pawn_xs = [2, 3, 4, 5]
        for x in pawn_xs:
            self.board.add_pieces([
                self._piece_factory.create_piece(PieceModel.PAWN, Vector2d(x, 1), 0),
                self._piece_factory.create_piece(PieceModel.PAWN, Vector2d(x, self.__BOARD_SIZE - 2), 1),
            ])
        self.board.add_pieces([
            self._piece_factory.create_piece(PieceModel.PAWN, Vector2d(0, 1), 0),
            self._piece_factory.create_piece(PieceModel.PAWN, Vector2d(self.__BOARD_SIZE - 1, self.__BOARD_SIZE - 2), 1)
        ])

    def __init_bishops(self):
        bishop_data = [
            (Vector2d(2, 0), 0), (Vector2d(5, 0), 0),
            (Vector2d(2, self.board.height - 1), 1), (Vector2d(5, self.board.height - 1), 1),
        ]
        for pos, color in bishop_data:
            self.__add_piece(self._piece_factory.create_piece(PieceModel.BISHOP, pos, color))

    def __init_rooks(self):
        rook_data = [
            (Vector2d(0, 0), 0), (Vector2d(7, 0), 0),
            (Vector2d(0, self.board.height - 1), 1), (Vector2d(7, self.board.height - 1), 1),
        ]
        for pos, color in rook_data:
            self.__add_piece(self._piece_factory.create_piece(PieceModel.ROOK, pos, color))

    def __init_knights(self):
        knight_data = [
            (Vector2d(1, 0), 0), (Vector2d(6, 0), 0),
            (Vector2d(1, self.board.height - 1), 1), (Vector2d(6, self.board.height - 1), 1),
        ]
        for pos, color in knight_data:
            self.__add_piece(self._piece_factory.create_piece(PieceModel.KNIGHT, pos, color))


    def move_piece(self, piece: Piece, destination: Vector2d) -> None:
        piece.move(destination)
        self.board.move_number = (self.board.move_number + 1) % 2
        # if self.board.move_number != piece.player_id:
        #     return
        #
        # piece_movement = self.board.get_piece_movement(piece.position)
        # moves = piece_movement.get_legal_moves()
        # for row in moves:
        #     if destination in row:
        #         piece.move(destination)
        #         self.board.move_number = (self.board.move_number + 1) % 2
        #         break
