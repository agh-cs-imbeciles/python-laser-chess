from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from utils import Vector2d
from game import CheckManager
from game.observer import PositionObserver
from game.piece import Piece, PieceModel
from game.piece.movement import Movement, PawnMovement
from game.piece.move import PieceMoveType, PieceMoveDetector

if TYPE_CHECKING:
    from game.piece.movement import PieceMovement


class Board(PositionObserver):
    def __init__(self, width: int, height: int):
        self._width: int = width
        self._height: int = height
        self._move_number: int = 0
        self._pieces: dict[Vector2d, tuple[Piece, PieceMovement]] = {}
        self._kings: list[Piece] = []
        self._check_manager = CheckManager(self)

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int) -> None:
        self._width = value

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int) -> None:
        self._height = value

    @property
    def move_number(self) -> int:
        return self._move_number

    @move_number.setter
    def move_number(self, value: int) -> None:
        self._move_number = value

    @property
    def pieces(self) -> dict[Vector2d, tuple[Piece, PieceMovement]]:
        return self._pieces

    @property
    def kings(self) -> list[Piece]:
        return self._kings

    # override PositionObserver
    def on_position_change(self, origin: Vector2d, destination: Vector2d) -> None:
        mp, op = self.get_piece(origin), self.get_piece(destination)
        self._pieces[destination] = self._pieces.pop(origin, None)
        self._check_manager.update()
        moveType: PieceMoveType = PieceMoveDetector.detect(self, mp, op)
        pass

    def get_size(self) -> tuple[int, int]:
        return self._width, self._height

    def get_piece(self, position: Vector2d) -> Optional[Piece]:
        piece = self._pieces.get(position)
        if piece is None:
            return None
        return piece[0]

    def get_piece_movement(self, position: Vector2d) -> Optional[PieceMovement]:
        piece = self._pieces.get(position)
        if piece is None:
            return None
        return piece[1]

    def can_move_to(self, destination: Vector2d, piece: Piece, capture: bool = False) -> bool:
        #
        # Check, if position after moving is in bounds of board
        #
        if destination.x < 0 or destination.x >= self.width or destination.y < 0 or destination.y >= self.height:
            return False
        #
        # Check, if player's king is under check - if it is, only covering moves are legal
        #
        if (
            piece.model != PieceModel.KING
            and self.is_king_under_check(piece.player_id)
            and self._check_manager.get_critical_square(destination, piece.player_id) is None
        ):
            return False

        #
        # Move with potential capturing
        #
        if capture:
            p = self.get_piece(destination)
            return p is None or p.player_id != piece.player_id
        #
        # Move without capturing
        #
        else:
            return not self.is_piece_at(destination)

    def is_piece_at(self, vector: Vector2d) -> bool:
        return self.get_piece(vector) is not None

    def is_check_at(self, position: Vector2d, player_id: int) -> bool:
        return self._check_manager.is_check_at(position, player_id)

    def add_piece(self, piece: tuple[Piece, PieceMovement]) -> None:
        if not self.get_piece(piece[0].position):
            self._pieces[piece[0].position] = piece
            piece[0].add_observer(self)

            if piece[0].model == PieceModel.KING:
                self._kings.append(piece[0])

    def add_pieces(self, pieces: list[tuple[Piece, PieceMovement]]) -> None:
        for piece in pieces:
            self.add_piece(piece)

    def get_player_all_moves(self):
        pass

    def is_king_under_check(self, player_id: int) -> bool:
        return self._check_manager.is_king_under_check(player_id)

    def add_critical_checked_squares(self, player_id: int, squares: list[Vector2d]) -> None:
        self._check_manager.add_critical_checked_squares(player_id, squares)

    # def check_squares(self, piece: Piece, origin: Vector2d, movement: Movement) -> list[Vector2d]:
    #     return self.__iterate_squares(piece, origin, movement)[0]
    #
    # def __check_squares_lmp(
    #     self, piece: Piece, origin: Vector2d, movement: Movement
    # ) -> tuple[list[Vector2d], Piece | None]:
    #     """
    #     Check squares of the board and return legal moves (lm) list and possible blocking piece (p).
    #     :param piece: piece involved
    #     :param origin: origin vector of ray checking
    #     :param movement: movement type of piece (rank, file, diagonal)
    #     :return: tuple of legal moves and optional piece, if is in the way of the ray
    #     """
    #
    #     legal_moves = []
    #     blocking_piece = None
    #     squares = Movement.get_squares(movement, self, origin)
    #
    #     for v in squares:
    #         if not self.can_move_to(v, piece):
    #             if self.is_piece_at(v) and piece.player_id != self.get_piece(v).player_id:
    #                 legal_moves.append(v)
    #                 blocking_piece = self.get_piece(v)
    #             break
    #         legal_moves.append(v)
    #
    #     return legal_moves, blocking_piece
    #
    # def __iterate_squares(self, piece: Piece, origin: Vector2d, movement: Movement) -> tuple[list[Vector2d], list[Piece]]:
    #     """
    #     Check squares of the board and return legal moves (lm) list and possible blocking piece (p).
    #     :param piece: piece involved
    #     :param origin: origin vector of ray checking
    #     :param movement: movement type of piece (rank, file, diagonal)
    #     :return: tuple of legal moves and optional piece, if is in the way of the ray
    #     """
    #
    #     found_player_piece = False
    #     legal_moves: list[Vector2d] = []
    #     pieces: list[Piece] = []
    #     squares = Movement.get_squares(movement, self, origin)
    #
    #     for v in squares:
    #         p = self.get_piece(v)
    #
    #         if self.can_move_to(v, piece) and len(pieces) == 0 and not found_player_piece:
    #             legal_moves.append(v)
    #         elif p and piece.player_id != p.player_id and not found_player_piece:
    #             if len(pieces) == 0:
    #                 legal_moves.append(v)
    #             pieces.append(self.get_piece(v))
    #         elif p and piece.player_id == p.player_id:
    #             found_player_piece = True
    #
    #     if len(pieces) >= 2 and pieces[1].model == PieceModel.KING:
    #         self._check_manager.pinned_pieces[pieces[1].player_id][pieces[0].position] = pieces[0]
    #
    #     return legal_moves, pieces
