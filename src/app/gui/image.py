from __future__ import annotations
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen


class PixelImage(Image):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.bind(on_kv_post=self.setup)

    def setup(self, pixel_image: PixelImage, screen: Screen) -> None:
        self.texture.mag_filter = "nearest"
        self.texture.min_filter = "nearest"
