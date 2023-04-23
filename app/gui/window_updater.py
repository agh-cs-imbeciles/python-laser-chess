from kivy.event import EventDispatcher
from kivy.uix.widget import Widget
from kivy.properties import DictProperty
from kivy.core.window import Window
from kivy.properties import NumericProperty

class WindowUpdater():
    def __init__(self,ids:DictProperty):
        self.elements = ids
        Window.bind(on_resize=self.on_resize)

    def on_resize(self, window, width, height):
        e = self.elements
        main_y = min(height,width / 1.2)
        # main_y = min(e.get('anchor').height, e.get('anchor').width/1.2)
        main_x = 1.2*main_y
        e.get('whole').width = main_x
        e.get('whole').height = main_y
        e.get('left_box').width = 0.2*main_x
        e.get('left_box').height = main_y
        e.get('board_addit').width = 0.8 * main_x
        e.get('board_addit').height = main_y
        e.get('top').height = 0.1 * main_y
        e.get('top').width = 0.6 * main_x
        e.get('bot').height = 0.1 * main_y
        e.get('bot').width = 0.6 * main_x
        e.get('mid').height = 0.8 * main_y
        e.get('mid').width = 0.8 * main_x
        e.get('left').width = 0.1 * main_x
        e.get('left').height = 0.8 * main_y
        e.get('right').width = 0.1 * main_x
        e.get('right').height = 0.8 * main_y
        e.get('board').width = 0.6 * main_x
        e.get('board').height = 0.8 * main_y


        # e.get('mid').width = 0.8*e.get('mid').parent.width



