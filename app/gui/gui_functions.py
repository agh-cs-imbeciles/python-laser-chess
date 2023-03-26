# returns path to image of piece on certain position
def _get_image_path(i: int, j: int) -> None | str:
    match i:
        case 0:
            match j:
                case 0 | 7:
                    return "assets/b_rook.png"
                case 1 | 6:
                    return "assets/b_knight.png"
                case 2 | 5:
                    return "assets/b_bishop.png"
                case 3:
                    return "assets/b_queen.png"
                case 4:
                    return "assets/b_king.png"
        case 1:
            return "assets/b_pawn.png"
        case 7:
            match j:
                case 0 | 7:
                    return "assets/w_rook.png"
                case 1 | 6:
                    return "assets/w_knight.png"
                case 2 | 5:
                    return "assets/w_bishop.png"
                case 3:
                    return "assets/w_queen.png"
                case 4:
                    return "assets/w_king.png"
        case 6:
            return "assets/w_pawn.png"
    return None