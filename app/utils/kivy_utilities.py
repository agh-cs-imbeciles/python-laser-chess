from typing import Any, Optional, Tuple

# converts rgb to kivy colour tuple
def RGBA_to_tuple(rgba: Tuple[int,int,int,int]) -> Tuple[float,float,float,float]:
    return rgba[0] / 255, rgba[1] / 255, rgba[2] / 255, rgba[3] / 255
