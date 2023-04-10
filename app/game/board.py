from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from utils import Vector2d
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
        self._checked_squares: list[dict[Vector2d, bool]] = [{}, {}]
        self._checking_pieces: list[dict[Vector2d, tuple[Piece, PieceMovement]]] = [{}, {}]

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
    def checked_squares(self):
        return self._checked_squares
    
    @checked_squares.setter
    def checked_squares(self, value: [dict[Vector2d, bool]]):
        self._checked_squares = value

    # override PositionObserver
    def on_position_change(self, origin: Vector2d, destination: Vector2d) -> None:
        mp, op = self.get_piece(origin), self.get_piece(destination)
        self._pieces[destination] = self._pieces.pop(origin, None)
        self.update_checked_squares()
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

    def can_move_to(self, to: Vector2d, piece: Optional[Piece] = None) -> bool:
        #
        # Check, if position after moving is in bounds of board
        #
        if to.x < 0 or to.x >= self.width or to.y < 0 or to.y >= self.height:
            return False

        #
        # Move with potential capturing
        #
        if isinstance(piece, Piece):
            p = self.get_piece(to)
            return True if not p or p.player_id != piece.player_id else False
        #
        # Move without capturing
        #
        else:
            return not self.is_piece_at(to)

    def is_piece_at(self, vector: Vector2d) -> bool:
        return self.get_piece(vector) is not None

    def is_check_at(self, piece: Piece) -> bool:
        return self._checked_squares[piece.player_id].get(piece.position) is not None

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
        if not 0 <= player_id < len(self._kings):
            raise ValueError("Invalid player id")
        return self._checked_squares[player_id].get(self._kings[player_id].position) is not None

    def update_checked_squares(self) -> None:
        for player_sqrs in self.checked_squares:
            player_sqrs.clear()

        for key, piece_data in self._pieces.items():
            #
            # Pawn capture moves
            #
            if isinstance(piece_data[1], PawnMovement):
                pos: Vector2d = piece_data[0].position + piece_data[1].direction
                for i, checked_squares in enumerate(self.checked_squares):
                    if piece_data[0].player_id == i: continue
                    checked_squares[pos + Vector2d(-1, 0)] = True
                    checked_squares[pos + Vector2d(1, 0)] = True
                continue

            #
            # Other pieces moves
            #
            for moves in piece_data[1].get_legal_moves():
                for move in moves:
                    for i, checked_squares in enumerate(self.checked_squares):
                        if piece_data[0].player_id == i: continue
                        p = self.get_piece(move)
                        if p is not None and p.model == PieceModel.KING and p.player_id != piece_data[0].player_id:
                            self._checking_pieces[p.player_id][move] = piece_data
                        checked_squares[move] = True

    def check_squares(self, piece: Piece, origin: Vector2d, movement: Movement) -> list[Vector2d]:
        return self.__check_squares_lmp(piece, origin, movement)[0]

    def __check_squares_lmp(
        self, piece: Piece, origin: Vector2d, movement: Movement
    ) -> tuple[list[Vector2d], Piece | None]:
        """
        Check squares of the board and return legal moves (lm) list and possible blocking piece (p).
        :param piece: piece involved
        :param origin: origin vector of ray checking
        :param movement: movement type of piece (rank, file, diagonal)
        :return: tuple of legal moves and optional piece, if is in the way of the ray
        """

        legal_moves = []
        blocking_piece = None
        squares = Movement.get_squares(movement, self, origin)

        for v in squares:
            if not self.can_move_to(v):
                if self.is_piece_at(v) and piece.player_id != self.get_piece(v).player_id:
                    legal_moves.append(v)
                    blocking_piece = self.get_piece(v)
                break
            legal_moves.append(v)

        return legal_moves, blocking_piece
