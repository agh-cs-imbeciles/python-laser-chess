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

# Piece model
# Colour
# Laser colour
# Direction


class ElementString(Enum):
    LASER = "laser"
    LASGUN = "lasgun_laser"
    MIRROR = "mirror_laser"
    PAWN = "pawn_laser"


class ColorString(Enum):
    WHITE = "white"
    BLACK = "black"


class OrientationString(Enum):
    TOP = "t"
    RIGHT = "r"
    BOTTOM = "b"
    LEFT = "l"


class LaserPainter:
    def __init__(self, board_view, board: Board, inverted: bool):
        self._board_view = board_view
        self._inverted = inverted
        self._board = board
        self._indicators = []

    def __inverse(self, direction: Movement | None) -> Movement | None:
        if direction is None:
            return None
        if self._inverted:
            return direction.double_right().double_right()
        return direction

    def _load(self, path: str, element: ElementString, rotation: Movement | None):
        image = RotatedImage(source=f"{Path.LASER_IMG_PATH}/{path}.png")
        rotation = self.__inverse(rotation)
        if element == ElementString.MIRROR:
            match rotation:
                case Movement.UPPER_LEFT_DIAGONAL:
                    image.angle = 90
                case Movement.UPPER_RIGHT_DIAGONAL:
                    image.angle = 0
                case Movement.BOTTOM_RIGHT_DIAGONAL:
                    image.angle = -90
                case Movement.BOTTOM_LEFT_DIAGONAL:
                    image.angle = -180
        if element == ElementString.LASER:
            match rotation:
                case Movement.UPPER_FILE | Movement.BOTTOM_FILE:
                    image.angle = 0
                case Movement.LEFT_RANK | Movement.RIGHT_RANK:
                    image.angle = 90
        if element == ElementString.LASGUN:
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

            #
            # Fields with lasguns
            #

            las = cast(Lasgun, las)
            if las.player_id == 0:
                piece = ElementString.LASGUN
                laser_color = ColorString.WHITE
            else:
                piece = ElementString.LASGUN
                laser_color = ColorString.BLACK
            string_value = f"{piece.value}_{laser_color.value}"
            self._indicators.append((self._load(string_value, ElementString.LASGUN, las.direction), las.position))

            direction = las.direction
            for f in fields:
                piece_real = cast(MirrorPiece, self._board.get_piece(f))
                if piece_real is None:
                    string_value = f"{ElementString.LASER.value}_{laser_color.value}"
                    self._indicators.append((self._load(string_value, ElementString.LASER, direction), f))
                else:
                    piece = ElementString.MIRROR
                    if piece_real.player_id == 0:
                        color = ColorString.WHITE
                    else:
                        color = ColorString.BLACK
                    string_value = f"{piece.value}_{color.value}_{laser_color.value}"
                    self._indicators.append((self._load(string_value, piece, piece_real.direction), piece_real.position))
                    direction = Movement.UPPER_FILE if Movement.LEFT_RANK == direction else Movement.LEFT_RANK
            hit = self._board.get_end_hit(las.player_id)
            if hit is None:
                continue
            piece_real = self._board.get_piece(hit[0])
            if piece_real.model == PieceModel.LASGUN:
                continue
            if piece_real.player_id == 0:
                color = ColorString.WHITE
            else:
                color = ColorString.BLACK
            rotation = self.__inverse(hit[1])

            if piece_real.model == PieceModel.PAWN:
                rotation_mirror = None
                piece = ElementString.PAWN
                match rotation:
                    case Movement.LEFT_RANK:
                        orientation = OrientationString.LEFT
                    case Movement.UPPER_FILE:
                        orientation = OrientationString.TOP
                    case Movement.RIGHT_RANK:
                        orientation = OrientationString.RIGHT
                    case Movement.BOTTOM_FILE:
                        orientation = OrientationString.BOTTOM
            elif piece_real.model == PieceModel.MIRROR:
                piece_real = cast(MirrorPiece, piece_real)
                rotation_mirror = self.__inverse(piece_real.direction)
                piece = ElementString.MIRROR
                # rotation
                match piece_real.direction:
                    case Movement.UPPER_LEFT_DIAGONAL:
                        if rotation == Movement.BOTTOM_FILE:
                            orientation = OrientationString.LEFT
                        else:
                            orientation = OrientationString.BOTTOM
                    case Movement.UPPER_RIGHT_DIAGONAL:
                        if rotation == Movement.LEFT_RANK:
                            orientation = OrientationString.LEFT
                        else:
                            orientation = OrientationString.BOTTOM
                    case Movement.BOTTOM_RIGHT_DIAGONAL:
                        if rotation == Movement.LEFT_RANK:
                            orientation = OrientationString.BOTTOM
                        else:
                            orientation = OrientationString.LEFT
                    case Movement.BOTTOM_LEFT_DIAGONAL:
                        if rotation == Movement.UPPER_FILE:
                            orientation = OrientationString.BOTTOM
                        else:
                            orientation = OrientationString.LEFT
            string_value = f"{piece.value}_{orientation.value}_{color.value}_{laser_color.value}"
            self._indicators.append((self._load(string_value, piece, rotation_mirror), hit[0]))

        for s, f in self._indicators:
            self._board_view._representations[f.y][f.x].add_widget(s)

    def clear(self):
        for ind in self._indicators:
            ind[0].parent.remove_widget(ind[0])
        self._indicators.clear()



