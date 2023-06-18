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

        font = main_x/25
        # CommonFontLabel.update_font(font)
        e.get("whole").size_hint = (None, None)
        # every element of board view is located in whole
        e.get('whole').width = main_x
        e.get('whole').height = main_y

        # promotion
        rpt = e.get('rotation_promotion_tab')
        # rpt.height = 0.2*e.get('left_box').height
        for rep in rpt.children:
            rep.width = rpt.width/len(rpt.children)
            rep.height = rep.width

        # Board background cells
        if e.get("board_images") is not None:
            bi = e.get("board_images")
            for i, j in [(i, j) for i in range(8) for j in range(8)]:
                bi[i, j].size = bi[i, j].parent.size

    def refresh(self):
        self.on_resize(None, None, None)