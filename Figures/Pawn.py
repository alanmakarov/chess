from Core.Square import Square
from Core.Color import Color
from Core.Interfaces import I_MovementContext
from Figures.Figure import Figure

class Pawn(Figure):

    def __init__(self, color: Color):
        super().__init__(color)
    
    def _check_ordinary_move_valide_area(self, start: Square, end: Square )-> bool:

        if start.ColIndex() == end.ColIndex():
            if self.Color == Color.WHITE: 
                if start.RowIndex() - end.RowIndex() == 1:
                    return True
                elif self.StepsCount == 0 and start.RowIndex() - end.RowIndex() == 2:
                    return True
            else:
                if end.RowIndex() - start.RowIndex() == 1:
                    return True
                elif self.StepsCount == 0 and end.RowIndex() - start.RowIndex() == 2:
                    return True

        return False
    
    def _check_attack_valide_area(self,start:Square,end:Square)->bool:
        if abs(start.ColIndex() - end.ColIndex()) == 1:
            if self.Color == Color.WHITE:
                if start.RowIndex() - end.RowIndex() == 1:
                    return True
            elif end.RowIndex() - start.RowIndex() == 1:
                return True
        
        return False


    def isValideMove(self, ctx: I_MovementContext) -> bool:

        if not self._is_valid_turn(ctx):
            return False
        
        start = ctx.current_position()
        end = ctx.new_position()

        if start == end:
            return False
        
        if self._check_ordinary_move_valide_area(start,end):
            return ctx.isPassEmpty()
        elif self._check_attack_valide_area(start, end):
            if ctx.isNewPositionPartnerOccupied(): # ordinary attack
                return True
            elif self.checkForEnPassantCase(ctx): # check for en passant case 
                return True
        
        return False


    def checkForEnPassantCase(self, ctx: I_MovementContext)-> bool :
        start = ctx.current_position()
        end = ctx.new_position()

        if ctx.isSquareEmpty(end):
            partner_spawn_square = Square(str(end.col)+str(start.row))
            figure1 = ctx.getFigure(partner_spawn_square)
            figure_prev = ctx.getPrevTurnFigure()
            
            if figure1 != None and figure1 == figure_prev and figure_prev.StepsCount == 1: 
                ctx.setEnPassantPawn(partner_spawn_square)
                return True
        
        return False


    def isValideAttack(self, ctx: I_MovementContext) -> bool:
        if self._check_attack_valide_area(ctx.current_position(), ctx.new_position()):
            return ctx.isNewPositionPartnerOccupied()
