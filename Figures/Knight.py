import re
from Context.Square import Square
from Context.Figure import Figure
from Context.Color import Color
from Context.MovementContext import I_MovementContext

class Knight(Figure):
    def __init__(self, color: Color):
        super().__init__(color)

    def __is_valid_jump(self,start:Square,end:Square)->bool:
        if abs(start.ColIndex() - end.ColIndex()) == 2 and abs(start.RowIndex() - end.RowIndex()) == 1:
            return True

        if abs(start.ColIndex() - end.ColIndex()) == 1 and abs(start.RowIndex() - end.RowIndex()) == 2:
            return True

        return False

    def isValideMove(self, ctx: I_MovementContext) -> bool:
        if self.__is_valid_jump(ctx.current_position(),ctx.new_position()):
            if ctx.isSquareEmpty(ctx.new_position()):
                return True
            elif ctx.isNewPositionPartnerOccupied():
                return True
        
        return False

        