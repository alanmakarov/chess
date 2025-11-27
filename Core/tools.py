from Core.Square import Square


def is_path_diagonal(self, start: Square,end: Square) -> bool:

    if start == end: 
        return False

    if start.ColIndex() - start.RowIndex() == end.ColIndex() - end.RowIndex():
        return True

    if start.ColIndex() + start.RowIndex() == end.ColIndex() + end.RowIndex():
        return True

    return False

def is_path_line(self, start: Square, end: Square) -> bool:

    if start == end: 
        return False

    if start.ColIndex() == end.ColIndex() or start.RowIndex() == end.RowIndex():
        return True
    else:
        return False