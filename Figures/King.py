from Figure import Figure
from Common.Color import Color
from Common.MovementContext import I_MovementContext
from Common.Square import Square


class King(Figure):
    def __init__(self, color: Color):
        super().__init__(color)


    def __check_valid_area(self,start:Square,end:Square)->bool:

        if start == end: 
            return False

        if abs(start.ColIndex() - end.ColIndex()) <= 1 and abs(start.RowIndex() - end.RowIndex()) <= 1 :
            return True
        
        return False

    
    def isValideMove(self, ctx: I_MovementContext) -> bool:
        if self._is_valid_turn(ctx) and self.__check_valid_area(ctx.current_position(),ctx.new_position()):
            if ctx.isPassEmpty(): 
                return True
            elif ctx.isNewPositionPartnerOccupied():
                return True

        return False  

    

