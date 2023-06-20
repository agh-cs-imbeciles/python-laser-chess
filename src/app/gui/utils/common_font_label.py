from kivy.uix.label import Label


class CommonFontLabel(Label):
    def __init__(self, **kwargs):
        self.font_modificator = kwargs.get("font_modificator")
        if self.font_modificator is None:
            self.font_modificator = 1
        else:
            kwargs.pop("font_modificator")
        super().__init__(**kwargs)

    def on_size(self,instance,value):
        self.font_size = self.font_modificator*self.width
