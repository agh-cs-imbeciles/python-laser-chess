from kivy.core.window import Window


class WindowUpdater:
    def __init__(self, ids: dict):
        self.elements = ids
        Window.bind(on_resize=self.on_resize)

        self.on_resize(None, 800, 600)

    def on_resize(self, window, width, height):
        e = self.elements
        main_y = min(height, width / 1.2)
        main_x = 1.2*main_y

        # every element of board view is located in whole

        e.get('whole').width = main_x
        e.get('whole').height = main_y

        # box with information about game + simple menu

        e.get('left_box').width = 0.2*main_x
        e.get('left_box').height = main_y

        # e.get('promotion_tab').width = 0.1*main_x
        # e.get('promotion_tab').height = 0.1*main_x
        # box with board and coordinates

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

        e.get('board').width = 0.6 * main_x
        e.get('board').height = 0.8 * main_y

        for rep in e.get('promotion_tab').children:
            rep.width = 0.2*main_x
            rep.height = 0.2*main_y

