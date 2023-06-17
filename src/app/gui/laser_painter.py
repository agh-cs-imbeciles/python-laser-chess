from typing import cast

from kivy.uix.image import Image
from enum import Enum
from app.gui import Path
from app.gui.utils import RotatedImage
from game import Board
from game.piece import PieceModel
from game.piece.lasgun import Lasgun, MirrorPiece
from game.piece.movement import Movement
from utils import BoardVector2d

class LaserRepresentationEnum(Enum):
    LASER = "/laser.png"
    LASGUN_BLACK = "/lasgun_laser_black.png"
    LASGUN_WHITE = "/lasgun_laser_white.png"
    MIRROR_BLACK = "/mirror_laser_black.png"
    MIRROR_WHITE = "/mirror_laser_white.png"
    PAWN_BLACK_BOTTOM = "/pawn_laser_b_black.png"
    PAWN_BLACK_TOP = "/pawn_laser_t_black.png"
    PAWN_BLACK_LEFT = "/pawn_laser_l_black.png"
    PAWN_BLACK_RIGHT = "/pawn_laser_r_black.png"
    PAWN_WHITE_BOTTOM = "/pawn_laser_b_white.png"
    PAWN_WHITE_TOP = "/pawn_laser_t_white.png"
    PAWN_WHITE_LEFT = "/pawn_laser_l_white.png"
    PAWN_WHITE_RIGHT = "/pawn_laser_r_white.png"


class LaserPainter:
    def __init__(self, board_view, board: Board):
        self._board_view = board_view
        self._board = board
        self._indicators = []

    @classmethod
    def _load(cls, rep_type: LaserRepresentationEnum, rotation: Movement):
        image = RotatedImage(source=f"{Path.LASER_IMG_PATH}{rep_type.value}")
        if rep_type == LaserRepresentationEnum.MIRROR_BLACK \
                or rep_type == LaserRepresentationEnum.MIRROR_WHITE:
            match rotation:
                case Movement.UPPER_LEFT_DIAGONAL:
                    image.angle = 90
                case Movement.UPPER_RIGHT_DIAGONAL:
                    image.angle = 0
                case Movement.BOTTOM_RIGHT_DIAGONAL:
                    image.angle = -90
                case Movement.BOTTOM_LEFT_DIAGONAL:
                    image.angle = -180
        if rep_type == LaserRepresentationEnum.LASER:
            match rotation:
                case Movement.UPPER_FILE:
                    image.angle = 0
                case Movement.LEFT_RANK:
                    image.angle = 90
        if rep_type == LaserRepresentationEnum.LASGUN_BLACK or rep_type == LaserRepresentationEnum.LASGUN_WHITE:
            match rotation:
                case Movement.UPPER_FILE:
                    image.angle = 0
                case Movement.LEFT_RANK:
                    image.angle = -90
                case Movement.RIGHT_RANK:
                    image.angle = 90
                case Movement.BOTTOM_FILE:
                    image.angle = 180

        if image:
            image.allow_stretch = True
            image.texture.min_filter = "nearest"
            image.texture.mag_filter = "nearest"
        return image

    def paint(self):
        lasguns = self._board.lasguns
        for las in lasguns:
            fields = self._board.get_laser_fields(las.player_id)
            if len(fields) == 0:
                continue
            las = cast(Lasgun,las)
            if las.player_id == 0:
                piece = LaserRepresentationEnum.LASGUN_WHITE
            else:
                piece = LaserRepresentationEnum.LASGUN_BLACK
            self._indicators.append((self._load(piece,las.direction),las.position))
            direction = las.direction
            for f in fields:
                piece = cast(MirrorPiece,self._board.get_piece(f))
                if piece is None:
                    self._indicators.append((self._load(LaserRepresentationEnum.LASER, direction), f))
                else:
                    if piece.player_id == 0:
                        value = LaserRepresentationEnum.MIRROR_WHITE
                    else:
                        value = LaserRepresentationEnum.MIRROR_BLACK
                    self._indicators.append((self._load(value,piece.direction),piece.position))
                    direction = Movement.UPPER_FILE if Movement.LEFT_RANK == direction else Movement.LEFT_RANK
            hit = self._board.get_end_hit(las.player_id)
            if hit is None:
                continue
            piece = self._board.get_piece(hit[0])
            if piece.model != PieceModel.PAWN:
                continue
            view = None
            if piece.player_id == 0:
                match hit[1]:
                    case Movement.LEFT_RANK:
                        view = LaserRepresentationEnum.PAWN_WHITE_LEFT
                    case Movement.UPPER_FILE:
                        view = LaserRepresentationEnum.PAWN_WHITE_TOP
                    case Movement.RIGHT_RANK:
                        view = LaserRepresentationEnum.PAWN_WHITE_RIGHT
                    case Movement.BOTTOM_FILE:
                        view = LaserRepresentationEnum.PAWN_WHITE_BOTTOM
            else:
                match hit[1]:
                    case Movement.LEFT_RANK:
                        view = LaserRepresentationEnum.PAWN_BLACK_LEFT
                    case Movement.UPPER_FILE:
                        view = LaserRepresentationEnum.PAWN_BLACK_TOP
                    case Movement.RIGHT_RANK:
                        view = LaserRepresentationEnum.PAWN_BLACK_RIGHT
                    case Movement.BOTTOM_FILE:
                        view = LaserRepresentationEnum.PAWN_BLACK_BOTTOM
            self._indicators.append((self._load(view, None), hit[0]))

        for s, f in self._indicators:
            self._board_view._representations[f.y][f.x].add_widget(s)

    def clear(self):
        for ind in self._indicators:
            ind[0].parent.remove_widget(ind[0])
        self._indicators.clear()



