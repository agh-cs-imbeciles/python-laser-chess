from __future__ import annotations
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.relativelayout import RelativeLayout
from enum import Enum
from app.gui import Path


# 0-white
class ImageButtonLayout(RelativeLayout):
    def __init__(self, src: str | None, button: Button, opacity=None):
        super().__init__()
        self._button = button
        self.add_widget(button)
        self._img = None
        # self._indicator = None
        if src is not None:
            self._img = Image(source=src)
            self._img.allow_stretch = True
            self._img.texture.mag_filter = "nearest"
            self.add_widget(self._img)
        if opacity is not None:
            self.opacity = opacity

    def __add_img_to_repr(self, img: Image):
        self.add_widget(img)

    def add_value_to_button(self, value):
        self._button.value = value

    def remove_img(self) -> Image | None:
        if self._img is None:
            return None
        img = self._img
        self.remove_widget(img)
        self._img = None
        return img

    def add_img(self, src: str):
        if self._img is not None:
            return
        img = Image(source=src)
        self._img = img
        self.__add_img_to_repr(img)


    # not used (yet)
    @property
    def img(self):
        return self._img



class Paths(Enum):
    LEFT  = f"{Path.IMG_PATH}/left.png"
    RIGHT = f"{Path.IMG_PATH}/right.png"

    def __str__(self):
        match self:
            case Paths.LEFT:
                return "L"
            case Paths.RIGHT:
                return "R"
