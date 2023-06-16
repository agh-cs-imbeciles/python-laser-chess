from typing import Tuple


# converts rgb to kivy colour tuple
def rgba_int_to_float(rgba: Tuple[int, int, int, int]) -> Tuple[float, float, float, float]:
    return rgba[0] / 255, rgba[1] / 255, rgba[2] / 255, rgba[3] / 255

