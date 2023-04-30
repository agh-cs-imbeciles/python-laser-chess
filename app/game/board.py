from __future__ import annotations

from builtins import list
from typing import TYPE_CHECKING, Optional
from utils import BoardVector2d
from game import CheckManager
from game.observer import PositionObserver
from game.piece import Piece, PieceModel
from game.piece.movement import Movement, PawnMovement
from game.piece.move import PieceMoveType, PieceMoveDetector
from game.promotion import PromotionManager
from game.piece.move.piece_move import PieceMove

if TYPE_CHECKING:
    from game import Game
    from game.piece.movement import PieceMovement


class Board(PositionObserver):
    def __init__(self, game: Game, width: int, height: int):
        self._width: int = width
        self._height: int = height
        self._move_number: int = 0
        self._pieces: dict[BoardVector2d, tuple[Piece, PieceMovement]] = {}
        self._kings: list[Piece] = []
        self._check_manager: CheckManager = CheckManager(self)
        self._game: Game = game
        self._promotion_manager = PromotionManager(self)

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
    def pieces(self) -> dict[BoardVector2d, tuple[Piece, PieceMovement]]:
        return self._pieces

    @property
    def kings(self) -> list[Piece]:
        return self._kings

    # override PositionObserver
    def on_position_change(self, origin: BoardVector2d, destination: BoardVector2d) -> None:
        mp, op = self.get_piece(origin), self.get_piece(destination)
        self._pieces[destination] = self._pieces.pop(origin, None)

        if mp is not None and mp.model == PieceModel.PAWN:
            pos = destination - self.get_piece_movement(destination).direction
            if self.is_piece_at(pos):
                self._pieces.pop(pos)

        self._check_manager.update()
        self._promotion_manager.check_promotion(mp)

        lm = self._game.get_last_move()
        if lm.move_type == PieceMoveType.QUEEN_SIDE_CASTLING or lm.move_type == PieceMoveType.KING_SIDE_CASTLING:
            self.move_number = (self.move_number + 1) % 2
            return

        piece_move: PieceMove = PieceMove(mp, origin, destination, None, None)
        self._game.add_move_to_history(piece_move)
        move_type: PieceMoveType = PieceMoveDetector.detect(self, mp, op, destination)
        self._game.modify_last_move(move_type=move_type)
        self._game.on_position_change(mp, move_type)
        if mp.model == PieceModel.QUEEN and mp.position == BoardVector2d(4, 4):
            pass

    def get_size(self) -> tuple[int, int]:
        return self._width, self._height

    def get_piece(self, position: BoardVector2d) -> Optional[Piece]:
        piece = self._pieces.get(position)
        if piece is None:
            return None
        return piece[0]

    def get_player_pieces_movements(self, player_id: int) -> list[tuple[Piece, PieceMovement]]:
        movements = []
        for piece, mov in self._pieces.values():
            if piece.is_same_color(player_id):
                movements.append((piece, mov))
        return movements

    def get_pieces_of(self, model: PieceModel, player_id: int) -> list[Piece]:
        pieces = []
        for _, pie in self._pieces.items():
            if pie[0].model == model and pie[0].player_id == player_id:
                pieces.append(pie[0])
        return pieces

    def get_piece_movement(self, position: BoardVector2d) -> Optional[PieceMovement]:
        piece = self._pieces.get(position)
        if piece is None:
            return None
        return piece[1]

    def is_out_of_bounds(self, destination: BoardVector2d) -> bool:
        return destination.x < 0 or destination.x >= self.width or destination.y < 0 or destination.y >= self.height

    def can_move_to(self, destination: BoardVector2d, piece: Piece, **kwargs) -> bool:
        """
        Verify, whether piece can move to the destination square.

        Options:
            Empty square.
            Empty square or enemy's piece.
            Enemy's piece obligatory.

        :param destination: ``BoardVector2d`` of desired destination square.
        :param piece: ``Piece`` which would change position.
        :param kwargs:
            capture: ``Boolean`` which defines optional capture.
            capture_required: ``Boolean`` which defines capture requirement (e.g. pawn capture).
        :return: ``Boolean`` of making a move.
        """
        # Aliases
        capture: bool = bool(kwargs.get("capture"))
        capture_required: bool = bool(kwargs.get("capture_required"))
        pid: int = piece.player_id

        #
        # Check, if position after moving is in bounds of board
        #
        if self.is_out_of_bounds(destination):
            return False
        #
        # Check, if player's king is under check - if it's, only covering moves are legal
        #
        if (
            piece.model != PieceModel.KING
            and self.is_king_under_check(pid)
            and self._check_manager.get_critical_square(destination, pid) is None
            and self._check_manager.checking_pieces[(pid + 1) % 2].get(destination) is None
        ):
            return False
        #
        # Check, if player can capture a checking piece
        #
        if (
            self._check_manager.checking_pieces[(pid + 1) % 2].get(destination) is not None
            and len(self._check_manager.checking_pieces[(pid + 1) % 2]) > 1
        ):
            return False
        #
        # Check, if piece isn't absolute pinned with own king
        #
        if (
            self._check_manager.pinned_pieces[pid].get(piece.position)
            and self._check_manager.pinned_pieces[pid].get(piece.position)[1] != self.get_piece(destination)
            and not self._check_manager.is_pinned_square(destination, pid)
        ):
            return False
        #
        # If it's a king, then check whether move destination isn't checked squares
        #
        if piece.model == PieceModel.KING and self.is_check_at(destination, piece.player_id):
            return False

        #
        # Move with potential capturing
        #
        if capture and not capture_required:
            p = self.get_piece(destination)
            return p is None or not p.is_same_color(pid)
        #
        # Move without capturing
        #
        elif not capture_required:
            return not self.is_piece_at(destination)
        #
        # Move with required capturing (e.g. pawn)
        #
        elif capture_required:
            p = self.get_piece(destination)
            return p is not None and not p.is_same_color(pid)

    def is_piece_at(self, position: BoardVector2d) -> bool:
        return self.get_piece(position) is not None

    def is_check_at(self, position: BoardVector2d, player_id: int) -> bool:
        return self._check_manager.is_check_at(position, player_id)

    def add_piece(self, piece: tuple[Piece, PieceMovement]) -> None:
        if not self.get_piece(piece[0].position):
            self._pieces[piece[0].position] = piece
            piece[0].add_observer(self)

            if piece[0].model == PieceModel.KING:
                self._kings.append(piece[0])

    def destroy_piece(self, piece: Piece):
        self._pieces.pop(piece.position, None)

    def add_pieces(self, pieces: list[tuple[Piece, PieceMovement]]) -> None:
        for piece in pieces:
            self.add_piece(piece)

    def get_to_promote(self) -> Piece | None:
        return self._promotion_manager.get_promotion_piece()

    def promote(self, model: PieceModel) -> tuple[Piece, PieceMovement] | None:
        new = self._promotion_manager.try_to_promote(model)
        if new is None:
            return
        self.add_piece(new)
        self._game.modify_last_move(promotion=new[0], move_type=PieceMoveType.PROMOTION)
        return new

    def get_possible_promotions(self) -> list[PieceModel]:
        return self._promotion_manager.get_possible_types()

    def get_player_all_moves(self):
        pass

    def is_king_under_check(self, player_id: int) -> bool:
        return self._check_manager.is_king_under_check(player_id)

    def get_ending_move(self) -> PieceMoveType | None:
        mn = (self._move_number + 1) % 2
        if self._check_manager.is_checkmate(mn):
            return PieceMoveType.CHECKMATE
        if self._check_manager.is_stalemate(mn):
            return PieceMoveType.STALEMATE
        return None

    def get_last_move(self):
        return self._game.get_last_move()

    def add_critical_checked_squares(self, player_id: int, squares: list[BoardVector2d]) -> None:
        self._check_manager.add_critical_checked_squares(player_id, squares)
