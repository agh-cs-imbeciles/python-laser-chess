from typing import Any
from utils import BoardVector2d, Paths
from game import Board
from game.piece import Piece, PieceModel, PieceFactory
from game.piece.move import PieceMove, PieceMoveType, PieceMoveDetector
from game.piece.movement import PieceMovement
from game.observer.game_end_obs import GameEndObserver
from game.notation_generator import  NotationGenerator
from game.ambiguous_enum import AmbiguousNotation
from game.piece.lasgun import MirrorDirections, MirrorPiece
from typing import cast

class Game:
    def __init__(self) -> None:
        self.__BOARD_SIZE: int = 8
        self._board: Board = Board(self, self.__BOARD_SIZE, self.__BOARD_SIZE)
        self._players: list[int] = []
        fill = PieceMove(move_type=PieceMoveType.MOVE)
        self._moves_history: list[list[PieceMove]] = [[fill], [fill]]
        self._last_move_index: tuple[int, int] = (0, 0)
        self._piece_factory = PieceFactory(self._board)
        self._observers: list[GameEndObserver] = []
        self.__init_board()
        self._notation_generator = NotationGenerator(self._board)
        self.add_observer(self._notation_generator)

    # override
    def on_position_change(self, piece: Piece, move_types: list[PieceMoveType]) -> None:
        if PieceMoveType.KING_SIDE_CASTLING in move_types:
            self.move_piece(
                self._board.get_piece(BoardVector2d(self.__BOARD_SIZE - 1, piece.position.y)),
                piece.position + BoardVector2d(-1, 0)
            )
            self._board.move_number = (self._board.move_number + 1) % 2
        elif PieceMoveType.QUEEN_SIDE_CASTLING in move_types:
            self.move_piece(
                self._board.get_piece(BoardVector2d(0, piece.position.y)),
                piece.position + BoardVector2d(1, 0)
            )
            self._board.move_number = (self._board.move_number + 1) % 2
        self.end_if_conditions_fulfilled()

    def set_notation_ambiguity(self, ambig: AmbiguousNotation) -> None:
        self._notation_generator.ambiguity = ambig

    def add_move_to_history(self, piece_move: PieceMove) -> None:
        mh = self._moves_history
        pid = piece_move.piece.player_id
        mh[pid].append(piece_move)
        self._last_move_index = piece_move.piece.player_id, len(mh[pid]) - 1

    def modify_last_move(self, piece: Piece = None, origin: BoardVector2d = None, destination: BoardVector2d = None,
                         promotion: Piece = None, move_type: list[PieceMoveType] = None, move: int = None) -> None:
        given = locals()
        given.pop('self')
        mh = self._moves_history
        lm = self._last_move_index
        last_move: PieceMove = mh[lm[0]][lm[1]]
        for key, val in given.items():
            if val is not None:
                setattr(last_move, key, val)

    def get_last_move(self):
        lmi = self._last_move_index
        return self._moves_history[lmi[0]][lmi[1]]

    def end_if_conditions_fulfilled(self) -> None:
        mov = self._board.get_ending_move()
        if mov is not None:
            for obs in self._observers:
                obs.on_end(self._board.move_number, mov)

    def add_observer(self, observer: GameEndObserver):
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
        # Mirrors
        self.__init_mirrors()

    def __init_kings(self):
        king_data = [
            (BoardVector2d(4, 0), 0),
            (BoardVector2d(4, self.board.height - 1), 1),
        ]
        for pos, color in king_data:
            self.__add_piece(self._piece_factory.create_piece(PieceModel.KING, pos, color))

    def __init_hetmanice(self):
        queen_data = [
            (BoardVector2d(3, 0), 0),
            (BoardVector2d(3, self.board.height - 1), 1),
        ]
        for pos, color in queen_data:
            self.__add_piece(self._piece_factory.create_piece(PieceModel.QUEEN, pos, color))

    def __init_pawns(self):
        pawn_xs = [2, 3, 4, 5]
        for x in pawn_xs:
            self.board.add_pieces([
                self._piece_factory.create_piece(PieceModel.PAWN, BoardVector2d(x, 1), 0),
                self._piece_factory.create_piece(PieceModel.PAWN, BoardVector2d(x, self.__BOARD_SIZE - 2), 1),
            ])
        self.board.add_pieces([
            self._piece_factory.create_piece(PieceModel.PAWN, BoardVector2d(0, 1), 0),
            self._piece_factory.create_piece(PieceModel.PAWN, BoardVector2d(self.__BOARD_SIZE - 1, self.__BOARD_SIZE - 2), 1)
        ])

    def __init_bishops(self):
        bishop_data = [
            (BoardVector2d(2, 0), 0), (BoardVector2d(5, 0), 0),
            (BoardVector2d(2, self.board.height - 1), 1), (BoardVector2d(5, self.board.height - 1), 1),
        ]
        for pos, color in bishop_data:
            self.__add_piece(self._piece_factory.create_piece(PieceModel.BISHOP, pos, color))

    def __init_rooks(self):
        rook_data = [
            (BoardVector2d(0, 0), 0), (BoardVector2d(7, 0), 0),
            (BoardVector2d(0, self.board.height - 1), 1), (BoardVector2d(7, self.board.height - 1), 1),
        ]
        for pos, color in rook_data:
            self.__add_piece(self._piece_factory.create_piece(PieceModel.ROOK, pos, color))

    def __init_knights(self):
        knight_data = [
            (BoardVector2d(1, 0), 0), (BoardVector2d(6, 0), 0),
            (BoardVector2d(1, self.board.height - 1), 1), (BoardVector2d(6, self.board.height - 1), 1),
        ]
        for pos, color in knight_data:
            self.__add_piece(self._piece_factory.create_piece(PieceModel.KNIGHT, pos, color))

    def __init_mirrors(self):
        mirror_data = [
            (BoardVector2d(3, 3), 0, MirrorDirections.UPPER_LEFT),
            (BoardVector2d(4, 3), 0, MirrorDirections.UPPER_RIGHT),
            (BoardVector2d(1, 1), 0, MirrorDirections.UPPER_LEFT),
            (BoardVector2d(6, 1), 0, MirrorDirections.UPPER_RIGHT),

            (BoardVector2d(3, 4), 1, MirrorDirections.BOTTOM_LEFT),
            (BoardVector2d(4, 4), 1, MirrorDirections.BOTTOM_RIGHT),
            (BoardVector2d(1, 6), 1, MirrorDirections.BOTTOM_LEFT),
            (BoardVector2d(6, 6), 1, MirrorDirections.BOTTOM_RIGHT),
        ]
        for pos, color, dir in mirror_data:
            self.__add_piece(self._piece_factory.create_piece(PieceModel.MIRROR, pos, color, dir))
        pass

    def move_piece(self, piece: Piece, destination: BoardVector2d, rotate_right: bool | None = None) -> None:
        ambig = self.board.ambiguity_move_type(self._board.get_piece_movement(piece.position), destination)
        self.set_notation_ambiguity(ambig)
        if rotate_right is not None and isinstance(piece, MirrorPiece):
            cast(MirrorPiece, piece).move(None, rotate_right)
        else:
            piece.move(destination)
        self.board.move_number = (self.board.move_number + 1) % 2
        #     return
        #
        # piece_movement = self.board.get_piece_movement(piece.position)
        # moves = piece_movement.get_legal_moves()
        # for row in moves:
        #     if destination in row:
        #         piece.move(destination)
        #         self.board.move_number = (self.board.move_number + 1) % 2
        #         break
