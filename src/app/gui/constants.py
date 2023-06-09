import os
import pathlib


class Path:
    CURRENT_PATH: str = pathlib.Path(__file__).parent.resolve()
    IMG_PATH: str = os.path.join(CURRENT_PATH, "../assets/images")
    PIECE_IMG_PATH: str = os.path.join(CURRENT_PATH, "../assets/images/board/pixel/wooden/pieces")
    WOODEN_IMG_PATH: str = os.path.join(CURRENT_PATH, "../assets/images/board/pixel/wooden")
    LASER_IMG_PATH: str = os.path.join(CURRENT_PATH, "../assets/images/board/pixel/wooden/laser")
