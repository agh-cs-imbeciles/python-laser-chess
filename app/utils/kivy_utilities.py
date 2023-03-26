from typing import Any, Optional, Tuple


def rgba_int_to_float(rgba: Tuple[int, int, int, int]) -> Tuple[float, float, float, float]:
    return rgba[0] / 255, rgba[1] / 255, rgba[2] / 255, rgba[3] / 255
