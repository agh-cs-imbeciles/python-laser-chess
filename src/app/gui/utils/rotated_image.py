from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.image import Image

Builder.load_string('''
<RotatedImage>:
    canvas.before:
        PushMatrix
        Rotate:
            angle: root.angle
            axis: 0, 0, 1
            origin: root.center
    canvas.after:
        PopMatrix
''')

class RotatedImage(Image):
    angle = NumericProperty()