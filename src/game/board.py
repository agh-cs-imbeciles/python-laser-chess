from __future__ import annotations
from builtins import list
from typing import TYPE_CHECKING, Optional, cast

from utils import BoardVector2d, Rotation
from game import CheckManager
from game.observer import PositionObserver, LaserObserver
from game.piece import Piece, PieceModel
from game.piece.lasgun import Lasgun
from game.piece.move import PieceMoveType, PieceMoveDetector
from game.promotion import PromotionManager
from game.piece.move.piece_move import PieceMove
from game.ambiguous_enum import AmbiguousNotation
import itertools

if TYPE_CHECKING:
    from game import Game
    from game.piece.movement import PieceMovement


class Board(PositionObserver, LaserObserver):


    def __init__(self, game: Game, width: int, height: int):
        self._width: int = width
        self._height: int = height
        self._move_number: int = 0
        self._pieces: dict[BoardVector2d, tuple[Piece, PieceMovement]] = {}
        self._kings: list[Piece] = []
        self._lasguns: list[Lasgun] = []
        self._check_manager: CheckManager = CheckManager(self)
        self._game: Game = game
        self._promotion_manager = PromotionManager(self)
        self._notation_list: list[str] = []

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

    def get_ambiguity_move_type(self, piece_movement: PieceMovement, destination: BoardVector2d) -> AmbiguousNotation:
        piece = piece_movement.piece
        same_pieces: list[Piece] = self.get_pieces_of(piece.model, piece.player_id)
        amb_f = set()
        pieces: list[Piece] = []
        if len(same_pieces) == 1:
            return AmbiguousNotation.NONE
        for p in same_pieces:
            if p == piece:
                pieces.append(p)
                continue
            mp = self.get_piece_movement(p.position)
            moves = list(itertools.chain.from_iterable(mp.get_legal_moves()))
            if destination in moves:
                pieces.append(p)
        if len(pieces) == 1:
            return AmbiguousNotation.NONE
        for i in range(len(pieces)):
            for j in range(i + 1, len(pieces)):
                if pieces[i].position.x != pieces[j].position.x and pieces[i].position.y != pieces[j].position.y:
                    continue
                if pieces[i].position.x == pieces[j].position.x:
                    amb_f.add(AmbiguousNotation.FILE)
                elif pieces[i].position.y == pieces[j].position.y:
                    amb_f.add(AmbiguousNotation.RANK)
        if len(amb_f) == 0:
            return AmbiguousNotation.NONE
        if len(amb_f) == 2:
            return AmbiguousNotation.BOTH
        if AmbiguousNotation.FILE in amb_f:
            return AmbiguousNotation.FILE
        return AmbiguousNotation.RANK

    def get_laser_fields(self):
        all_las = []
        for las in self._lasguns:
            all_las.extend(las.laser_fields)
        return all_las

    def laser_fire_conditions(self, player_id: int):
        for las in self.lasguns:
            if las.player_id == player_id:
                las.use_laser()

    def on_laser_propagated(self, lasgun: Lasgun) -> None:
        for field in lasgun.laser_fields:
            pc = self.get_piece(field)
            if pc is not None and pc.model != PieceModel.MIRROR:
                self.destroy_piece(pc)
        self._game.end_if_conditions_fulfilled()

    def on_rotation(self, origin: BoardVector2d, rotation: Rotation) -> None:
        mp = self.get_piece(origin)

        #
        # Propagating laser fields
        #
        for las in self._lasguns:
            las.propagate_until_target()
            if not las.fired:
                las.charge()

        #
        # Analyzing move for PieceMoveType and generating notation
        #
        piece_move: PieceMove = PieceMove(mp, origin,origin, rotation=rotation)
        self._game.add_move_to_history(piece_move)
        move_types: list[PieceMoveType] = [PieceMoveType.ROTATION]
        self._game.get_last_move().add_move_type(move_types)
        self._game.on_position_change(mp, move_types)
        self._notation_list.append(self._game._notation_generator.generate_last_move_string())

    # override PositionObserver
    def on_position_change(self, origin: BoardVector2d, destination: BoardVector2d) -> None:
        #
        # Move piece
        #
        mp, op = self.get_piece(origin), self.get_piece(destination)
        self._pieces[destination] = self._pieces.pop(origin, None)
        if mp is not None and op is None and mp.model == PieceModel.PAWN:
            pos = destination - self.get_piece_movement(destination).direction
            if self.is_piece_at(pos):
                self._pieces.pop(pos)

        #
        # Propagating laser fields
        #
        for las in self._lasguns:
            las.propagate_until_target()
            if not las.fired:
                las.charge()

        #
        # Updating check and promotion managers
        #
        self._check_manager.update()
        self._promotion_manager.check_promotion(mp)

        #
        # Analyzing move for PieceMoveType and generating notation
        #
        lm = self._game.get_last_move()
        if PieceMoveType.QUEEN_SIDE_CASTLING in lm.move_types or PieceMoveType.KING_SIDE_CASTLING in lm.move_types:
            return
        piece_move: PieceMove = PieceMove(mp, origin, destination, None, None)
        self._game.add_move_to_history(piece_move)
        move_types: list[PieceMoveType] = PieceMoveDetector.detect(self, mp, op, destination)
        self._game.get_last_move().add_move_type(move_types)
        if PieceMoveType.PROMOTION in move_types:
            self._game.get_last_move().add_promotion_piece(self.get_to_promote())
        self._game.on_position_change(mp, move_types)
        self._notation_list.append(self._game._notation_generator.generate_last_move_string())

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
        # Check, if laser blocks movement
        #
        if piece.model != PieceModel.MIRROR and piece.model != PieceModel.PAWN and \
                destination in self.get_laser_fields():
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
        # If it's a king and on the destination square is the checking piece,
        # then check whether the checking piece is protected
        #
        elif (
                self._check_manager.checking_pieces[(pid + 1) % 2].get(destination) is not None
                and piece.model == PieceModel.KING
                and self._check_manager.is_piece_protected(self.get_piece(destination))
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
            if piece[0].model == PieceModel.LASGUN:
                self._lasguns.append(piece[0])
                piece[0].add_laser_observer(self)

    def destroy_piece(self, piece: Piece):
        if piece is None:
            return
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
        self._check_manager.update()
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
        if self._check_manager.is_king_dead(mn):
            return PieceMoveType.LASER_MATE
        return None

    def get_last_move(self):
        return self._game.get_last_move()

    def add_critical_checked_squares(self, player_id: int, squares: list[BoardVector2d]) -> None:
        self._check_manager.add_critical_checked_squares(player_id, squares)

    @property
    def lasguns(self):
        return self._lasguns
