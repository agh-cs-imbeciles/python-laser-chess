from typing import cast

from kivy.properties import NumericProperty
from kivy.uix.label import Label
import weakref



class CommonFontLabel(Label):
    instances = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__class__.instances.append(weakref.proxy(self))

    @classmethod
    def update_font(cls, size: int):
        for i in cls.instances:
            cast(CommonFontLabel, i).font_size = size
