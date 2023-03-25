class Board:
    def __init__(self, width, height, player_ids):
        self._width = width
        self._height = height
        self._pieces = {id: {} for id in player_ids}

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = value

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        self._height = value

    def get_size(self):
        return self._width, self._height
