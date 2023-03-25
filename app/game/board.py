class Board:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._move_number = 0
        self._pieces = {}
        self._moves_history = []

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
        
    @property
    def move_number(self):
        return self._move_number
    
    @move_number.setter
    def move_number(self, value):
        self._move_number = value
        
    @property
    def moves_history(self):
        return self._moves_history
    
    @moves_history.setter
    def moves_history(self, value):
        self._moves_history = value

    def get_size(self):
        return self._width, self._height

    def get_piece(self, position):
        return self._pieces.get(position)

    def can_move_to(self, to, piece=None):
        #
        # Check, if position after moving is in bounds of board
        #
        if to.x < 0 or to.x >= self.width or to.y < 0 or to.y >= self.height:
            return False

        #
        # Move with potential capturing
        #
        if piece is not None:
            return True if not self.get_piece(to) or self.get_piece(to).player_id != piece.player_id else False
        #
        # Move without capturing
        #
        else:
            return True if not self.get_piece(to) else False

    def add_piece(self, piece):
        if not self.get_piece(piece.position):
            self._pieces[piece.position] = piece

    def add_pieces(self, pieces):
        for piece in pieces:
            self.add_piece(piece)
