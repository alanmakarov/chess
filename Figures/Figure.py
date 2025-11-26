from abc import ABC, abstractmethod
from Core.Square import Square
from Core.Interfaces import I_MovementContext
from Core.Interfaces import I_Figure
from Core.Color import Color


class Figure(I_Figure):
    
    def __init__(self, color : Color):
        self.__color = color
        self.__stepsCount = 0

    def _is_pass_diagonal(self, start: Square,end: Square) -> bool:

        if start == end: 
            return False

        if start.ColIndex() - start.RowIndex() == end.ColIndex() - end.RowIndex():
            return True

        if start.ColIndex() + start.RowIndex() == end.ColIndex() + end.RowIndex():
            return True

        return False
    
    def _is_pass_line(self, start: Square, end: Square) -> bool:

        if start == end: 
            return False

        if start.ColIndex() == end.ColIndex() or start.RowIndex() == end.RowIndex():
            return True
        else :
            return False

    def _is_valid_turn(self, ctx: I_MovementContext)-> bool:
        return ctx.turnColor() == self.__color

    def ConfirmMove(self):
        self.__stepsCount +=1

    @property
    def StepsCount(self):
        return self.__stepsCount

    @property
    def Color(self):
        return self.__color

    def __str__(self):
        return str(self.__color)+"_"+self.__class__.__name__

    def copy(self):
        return self.__class__(self.__color)

    @abstractmethod
    def isValideMove(self, ctx: I_MovementContext) -> bool: ...
    
    def isValideAttack(self, ctx: I_MovementContext) -> bool:
        if ctx.isNewPositionPartnerOccupied():
            return self.isValideMove(ctx)
        return False


