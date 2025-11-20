from Color import Color
from Square import Square
from Interfaces import I_Figure
from Figures.Figure import Figure

class BoardStorage:
    def __init__(self, data = None) -> None:
        if isinstance(data, BoardStorage):
            self.__matr = [ [ None if el is None else el.copy() for el in row ] for row in data.__matr]
        elif data == None:
            self.__matr = [[None for _ in range(8)] for _ in range(8)]
        else:
            raise TypeError(f'Expected BoardStorage or None, got {type(data).__name__}')

    def getClone(self):
        return BoardStorage(self)

    def __getitem__(self,square:Square):
        if isinstance(square, Square):
            return self._matr[square.x][square.y]
        return NotImplemented

    def __setitem__(self,square, figure):
        if isinstance(square, Square) and isinstance(figure, I_Figure) :
            self._matr[square.x][square.y] = figure
        return NotImplemented


    def get_line(self, start: Square, stop: Square) -> list :
        if start.x == stop.x :
            if start.y <= stop.y:
                return self._matr[start.x][start.y:stop.y+1]
            else:
                return self._matr[start.x][start.y:stop.y-1:-1]
        elif start.y==stop.y:
            if start.x <= stop.x:
                return [self._matr[i][start.y] for i in range(start.x,stop.x+1) ]
            else:
                return [self._matr[i][start.y] for i in range(start.x,stop.x-1,-1) ]
        else:
            raise ValueError("не на одной")
        
    def _check_coordinates(self, start: Square, stop: Square) -> bool:
        if start.x-start.y == stop.x - stop.y : 
            return False 
        elif start.x+start.y == stop.x + stop.y :
            return False
        
        return (True,None)
    def get_diag(self, start: Square, stop: Square) -> list :

        err = self._check_coordinates(start,stop)
        if err :
            raise ValueError(f'Incorrect path: {str(start)},{str(stop)}')

        start_row, start_col = start.x, start.y
        end_row, end_col = stop.x, stop.y
    
        row_step = -1 if start_row > end_row else 1
        col_step = -1 if start_col > end_col else 1
    
        rows = range(start_row, end_row + row_step, row_step)
        cols = range(start_col, end_col + col_step, col_step)

        elements = [self._matr[row][col] for row, col in zip(rows, cols)]
    
        return elements

    def get_king_square(self, color: Color)-> Square:
        raise NotImplemented

    def get_occupied_coordinates(self,color: Color) -> list:
        raise NotImplemented