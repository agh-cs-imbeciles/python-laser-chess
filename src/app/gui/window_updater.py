from copy import deepcopy
from typing import cast

from kivy.core.window import Window
from kivy.graphics import Color, Rectangle

from app.gui.utils.common_font_label import CommonFontLabel


class WindowUpdater:
    def __init__(self, elements_dict: dict):
        self.elements = elements_dict
        Window.bind(on_resize=self.on_resize)
        Window.clearcolor = (.1, .1, .1, 1)
        self.on_resize(None, None, None)

    def on_resize(self, a, b, c):
        width = Window.width
        height = Window.height
        e = self.elements
        main_y = min(height, width / 1.48)
        main_x = 1.48*main_y


        e.get("whole").size_hint = (None, None)
        e.get('whole').width = main_x
        e.get('whole').height = main_y


    def refresh(self):
        self.on_resize(None, None, None)