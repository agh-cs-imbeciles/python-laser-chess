from __future__ import annotations
from typing import Any
from typing import cast

from utils import BoardVector2d, Rotation, GameEnding
from game import Board
from game.piece import Piece, PieceModel, PieceFactory
from game.piece.move import PieceMove, PieceMoveType, PieceMoveDetector
from game.piece.movement import PieceMovement, Movement
from game.observer.game_end_obs import GameEndObserver
from game.notation_generator import NotationGenerator
from game.ambiguous_enum import AmbiguousNotation
from game.piece.lasgun import MirrorPiece


class Game:
    def __init__(self) -> None:
        self.__BOARD_SIZE: int = 8
        self._board: Board = Board(self, self.__BOARD_SIZE, self.__BOARD_SIZE)
        self._board_view = None
        self._players: list[int] = []
        self._move_number: int = 0
        fill = PieceMove(move_type=PieceMoveType.MOVE)
        self._moves_history: list[list[PieceMove]] = [[fill], [fill]]
        self._last_move_index: tuple[int, int] = (0, 0)
        self._piece_factory = PieceFactory(self._board)
        self._observers: list[GameEndObserver] = []
        self.__init_board()
        self._notation_generator = NotationGenerator(self._board)
        self.add_observer(self._notation_generator)

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
    def move_number(self) -> int:
        return self._move_number

    @property
    def moves_history(self) -> list[Any]:
        return self._moves_history

    @property
    def board_view(self, board_view: Board):
        return self._board_view

    @board_view.setter
    def board_view(self, board_view: Board):
        self._board_view = board_view

    # override
    def on_position_change(self, piece: Piece, move_types: list[PieceMoveType]) -> None:
        if PieceMoveType.KING_SIDE_CASTLING in move_types:
            self.move_piece(
                self._board.get_piece(BoardVector2d(self.__BOARD_SIZE - 1, piece.position.y)),
                piece.position + BoardVector2d(-1, 0)
            )
            self._move_number = (self._move_number + 1) % 2
        elif PieceMoveType.QUEEN_SIDE_CASTLING in move_types:
            self.move_piece(
                self._board.get_piece(BoardVector2d(0, piece.position.y)),
                piece.position + BoardVector2d(1, 0)
            )
            self._move_number = (self._move_number + 1) % 2

        mov = self._board.get_ending_move()
        if mov is not None:
            winner = (self._move_number + 1) % 2
            match mov:
                case PieceMoveType.CHECKMATE:
                    end = GameEnding.CHECKMATE
                case PieceMoveType.STALEMATE:
                    end = GameEnding.STALEMATE
                    winner = None
                case PieceMoveType.LASER_MATE:
                    end = GameEnding.LASER_MATE
            self.end_game(winner, end)

    def set_notation_ambiguity(self, ambig: AmbiguousNotation) -> None:
        self._notation_generator.ambiguity = ambig

    def add_move_to_history(self, piece_move: PieceMove) -> None:
        mh = self._moves_history
        pid = piece_move.piece.player_id
        mh[pid].append(piece_move)
        self._last_move_index = piece_move.piece.player_id, len(mh[pid]) - 1

    def modify_last_move(self, **kwargs) -> None:
        mh = self._moves_history
        lm = self._last_move_index
        last_move: PieceMove = mh[lm[0]][lm[1]]
        for key, val in kwargs.items():
            if val is not None:
                setattr(last_move, key, val)

    def get_last_move(self) -> PieceMove:
        lmi = self._last_move_index
        return self._moves_history[lmi[0]][lmi[1]]

    def end_game(self, winner: int | None, game_ending: GameEnding) -> None:
        for obs in self._observers:
            obs.on_end(winner, game_ending)

    def add_observer(self, observer: GameEndObserver) -> None:
        self._observers.append(observer)

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
        # Lasguns
        self.__init_lasguns()

    def __init_kings(self) -> None:
        king_data = [
            (BoardVector2d(4, 0), 0),
            (BoardVector2d(4, self.board.height - 1), 1),
        ]
        for pos, color in king_data:
            self.__add_piece(self._piece_factory.create_piece(PieceModel.KING, pos, color))

    def __init_hetmanice(self) -> None:
        queen_data = [
            (BoardVector2d(3, 0), 0),
            (BoardVector2d(3, self.board.height - 1), 1),
        ]
        for pos, color in queen_data:
            self.__add_piece(self._piece_factory.create_piece(PieceModel.QUEEN, pos, color))

    def __init_pawns(self) -> None:
        pawn_xs = [2, 3, 4, 5]
        for x in pawn_xs:
            self.board.add_pieces([
                self._piece_factory.create_piece(PieceModel.PAWN, BoardVector2d(x, 1), 0),
                self._piece_factory.create_piece(PieceModel.PAWN, BoardVector2d(x, self.__BOARD_SIZE - 2), 1),
            ])
        self.board.add_pieces([
            self._piece_factory.create_piece(PieceModel.PAWN, BoardVector2d(0, 1), 0),
            self._piece_factory.create_piece(PieceModel.PAWN,
                                             BoardVector2d(self.__BOARD_SIZE - 1, self.__BOARD_SIZE - 2), 1)
        ])

    def __init_bishops(self) -> None:
        bishop_data = [
            (BoardVector2d(2, 0), 0), (BoardVector2d(5, 0), 0),
            (BoardVector2d(2, self.board.height - 1), 1), (BoardVector2d(5, self.board.height - 1), 1),
        ]
        for pos, color in bishop_data:
            self.__add_piece(self._piece_factory.create_piece(PieceModel.BISHOP, pos, color))

    def __init_rooks(self) -> None:
        rook_data = [
            (BoardVector2d(0, 0), 0), (BoardVector2d(7, 1), 0),
            (BoardVector2d(0, self.board.height - 2), 1), (BoardVector2d(7, self.board.height - 1), 1),
        ]
        for pos, color in rook_data:
            self.__add_piece(self._piece_factory.create_piece(PieceModel.ROOK, pos, color))

    def __init_knights(self) -> None:
        knight_data = [
            (BoardVector2d(1, 0), 0), (BoardVector2d(6, 0), 0),
            (BoardVector2d(1, self.board.height - 1), 1), (BoardVector2d(6, self.board.height - 1), 1),
        ]
        for pos, color in knight_data:
            self.__add_piece(self._piece_factory.create_piece(PieceModel.KNIGHT, pos, color))

    def __init_mirrors(self) -> None:
        mirror_data = [
            (BoardVector2d(3, 3), 0, Movement.UPPER_LEFT_DIAGONAL),
            (BoardVector2d(4, 3), 0, Movement.UPPER_RIGHT_DIAGONAL),
            (BoardVector2d(1, 1), 0, Movement.UPPER_LEFT_DIAGONAL),
            (BoardVector2d(6, 1), 0, Movement.UPPER_RIGHT_DIAGONAL),

            (BoardVector2d(3, 4), 1, Movement.BOTTOM_LEFT_DIAGONAL),
            (BoardVector2d(4, 4), 1, Movement.BOTTOM_RIGHT_DIAGONAL),
            (BoardVector2d(1, 6), 1, Movement.BOTTOM_LEFT_DIAGONAL),
            (BoardVector2d(6, 6), 1, Movement.BOTTOM_RIGHT_DIAGONAL),
        ]
        for pos, color, dir in mirror_data:
            self.__add_piece(self._piece_factory.create_piece(PieceModel.MIRROR, pos, color, dir))

    def __init_lasguns(self) -> None:
        lasgun_data = [
            (BoardVector2d(7, 0), 0, Movement.UPPER_FILE),
            (BoardVector2d(0, self._board.height - 1), 1, Movement.BOTTOM_FILE),
        ]
        for pos, color, dir in lasgun_data:
            self.__add_piece(self._piece_factory.create_piece(PieceModel.LASGUN, pos, color, dir))

    def move_piece(self, piece: Piece, destination: BoardVector2d, rotate: Rotation | None = None) -> None:
        ambig = self.board.get_ambiguity_move_type(self._board.get_piece_movement(piece.position), destination)
        self.set_notation_ambiguity(ambig)
        if rotate is not None and isinstance(piece, MirrorPiece):
            cast(MirrorPiece, piece).move(piece.position, rotate)
        else:
            piece.move(destination)
        self._move_number = (self._move_number + 1) % 2

    def set_time(self, player_id: int, seconds: int):
        if seconds == 0:
            # end game
            pass
        minutes = seconds // 60
        seconds = seconds % 60
        if self._board_view is None:
            return
        self._board_view.set_time(player_id, f"{minutes}:{seconds:02d}")
