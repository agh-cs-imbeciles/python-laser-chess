from copy import deepcopy
from kivy.core.window import Window


class WindowUpdater:
    def __init__(self, elements_dict: dict):
        self.elements = elements_dict
        Window.bind(on_resize=self.on_resize)
        self.on_resize(None, None, None)

    def on_resize(self, a, b, c):
        width = Window.width
        height = Window.height
        e = self.elements
        main_y = min(height, width / 1.2)
        main_x = 1.2*main_y

        # every element of board view is located in whole
        e.get('whole').width = main_x
        e.get('whole').height = main_y

        # box with information about game + simple menu
        e.get('left_box').width = 0.2*main_x
        e.get('left_box').height = main_y

        e.get('board_addit').width = 0.8 * main_x
        e.get('board_addit').height = main_y

        # box with top coordinates
        e.get('top').height = 0.1 * main_y
        e.get('top').width = 0.6 * main_x

        # box with bottom coordinates
        e.get('bot').height = 0.1 * main_y
        e.get('bot').width = 0.6 * main_x

        # box with board, left and right coordinates
        e.get('mid').height = 0.8 * main_y
        e.get('mid').width = 0.8 * main_x

        # box with left coordinates
        e.get('left').width = 0.1 * main_x
        e.get('left').height = 0.8 * main_y

        # box with right coordinates
        e.get('right').width = 0.1 * main_x
        e.get('right').height = 0.8 * main_y

        # board
        b_size = max(0.6 * main_x, 0.8 * main_y)
        e.get('board').width = b_size
        e.get('board').height = b_size

        e.get('indicator_lab').height = 10

        # promotion
        rpt = e.get('rotation_promotion_tab')
        rpt.height = 0.2*e.get('left_box').height
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