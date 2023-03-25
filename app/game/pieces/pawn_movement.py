from piece_movement import PieceMovement
# from piece import Piece
# from piece_model import PieceModel
# from game.board import Board
# from utils.vector2d import Vector2d


class PawnMovement(PieceMovement):
    def __init__(self, pawn, board, direction, en_passant_position, promotion_position):
        super().__init__(pawn, board)
        self._initial_position = pawn.position.copy
        self._direction = direction
        self._en_passant_position = en_passant_position
        self._promotion.position = promotion_position

    # override
    def get_legal_moves(self):
        self._legal_moves.clear()
        b = self._board
        p = self._piece
        dir = self._direction

        #
        # Advance 1 square (default move)
        #
        if b.can_move_to(p.position + dir, p):
            self._legal_moves.append(p.position + dir)
        #
        # Advance 2 squares (first move)
        #
        if p.position == self._initial_position and b.can_move_to(p.position + dir.multiply_scalar(2), p):
            self._legal_moves.append(p.position + dir.multiply_scalar(2))
        #
        # En passant
        #
        if p.position == self._en_passant_position:
            #
            # En passant (left)
            #
            if b.get_piece(p.position - dir.reverse_axis()) and b.can_move_to(p.position - dir.reverse_axis()):
                self._legal_moves.append(p.position - dir.reverse_axis())
            #
            # En passant (right)
            #
            if b.get_piece(p.position + dir.reverse_axis()) and b.can_move_to(p.position + dir.reverse_axis()):
                self._legal_moves.append(p.position + dir.reverse_axis())
