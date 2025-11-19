import unittest
import io
from Figures.Pawn import Pawn
from Figures.Figure import Figure
from Common.MovementContext import I_MovementContext
from Common.Square import Square
from Common.Color import Color

class TestContext(I_MovementContext):
    def __init__(self, start: Square, end: Square, emptyPath = True, PartnerFigureInEndPos = False) -> None:
        self.start = start
        self.end = end
        self._passEmpty = emptyPath
        self._PartnerfigureInEndPos = PartnerFigureInEndPos
        self.PrevPawn = None
        self.SquareEnPassant = None
        self.TurnColor = Color.WHITE

    def current_position(self) -> Square:
        return self.start
    def new_position(self) -> Square:
        return self.end
    def turnColor(self) -> Color:
        return self.TurnColor
    def isSquareEmpty(self, square) -> bool:
        return True
    def isPassEmpty(self) -> bool:
        return self._passEmpty
    def isNewPositionPartnerOccupied(self) -> bool:
        return self._PartnerfigureInEndPos
    def getFiguresOnPassAmmount(self) -> int:
        return 1 if self._PartnerfigureInEndPos else 0
    def getFigure(self, square: Square) -> Figure:
        return self.PrevPawn
    def getPrevTurnFigure(self) -> Figure:
        return self.PrevPawn
    def setEnPassantPawn(self, square: Square):
        self.SquareEnPassant = square

    
class TestPawn(unittest.TestCase):
    def setUp(self) -> None:
        self.BlackPawn = Pawn(Color.BLACK)
        self.WhitePawn = Pawn(Color.WHITE)
        
    def test_PawnCorrectMove(self):
        ctx1 = TestContext(Square("b2"),Square("b3"))
        ctx2 = TestContext(Square("b2"),Square("b4"))

        ctx3 = TestContext(Square("b7"),Square("b6"))
        ctx4 = TestContext(Square("b7"),Square("b5"))
        ctx3.TurnColor = Color.BLACK
        ctx4.TurnColor = Color.BLACK

        self.assertTrue(self.WhitePawn.isValideMove(ctx1))
        self.assertTrue(self.WhitePawn.isValideMove(ctx2))
        self.assertTrue(self.BlackPawn.isValideMove(ctx3))
        self.assertTrue(self.BlackPawn.isValideMove(ctx4))

        attack_ctx = TestContext(Square("b2"),Square("c3"),emptyPath= False, PartnerFigureInEndPos = True)
        self.assertTrue(self.WhitePawn.isValideMove(attack_ctx)) 

    def test_PawnIncorrectMove(self):
        ctx1 = TestContext(Square("b2"),Square("a3"))
        ctx2 = TestContext(Square("b2"),Square("b3"),False,True)
        ctx3 = TestContext(Square("b2"),Square("b4"),False,False)
        
        ctx4 = TestContext(Square("b7"),Square("b6"))
        ctx5 = TestContext(Square("b2"),Square("b3"))
        ctx5.TurnColor = Color.BLACK

        self.assertFalse(self.WhitePawn.isValideMove(ctx1))
        self.assertFalse(self.WhitePawn.isValideMove(ctx2))
        self.assertFalse(self.WhitePawn.isValideMove(ctx3))
        self.assertFalse(self.WhitePawn.isValideMove(ctx4))

        self.assertFalse(self.BlackPawn.isValideMove(ctx5)) 

    def test_PawnAttack(self):
        attack_ctx1 = TestContext(Square("b7"),Square("c6"),emptyPath= False, PartnerFigureInEndPos = True)
        attack_ctx2 = TestContext(Square("b7"),Square("a6"),emptyPath= False, PartnerFigureInEndPos = True)
        attack_ctx1.TurnColor = Color.BLACK
        attack_ctx2.TurnColor = Color.BLACK


        self.assertTrue(self.BlackPawn.isValideAttack(attack_ctx1)) 
        self.assertTrue(self.BlackPawn.isValideAttack(attack_ctx2)) 
    
    def test_forEnPassant(self):
        ctx1 = TestContext(Square("b4"),Square("c3"),emptyPath= False, PartnerFigureInEndPos = False)
        ctx1.TurnColor = Color.BLACK
        ctx1.PrevPawn = Pawn(Color.WHITE)
        ctx1.PrevPawn.ConfirmMove()

        self.assertTrue(self.BlackPawn.isValideMove(ctx1))
        self.assertEqual(Square("c4"),ctx1.SquareEnPassant)

        ctx2 = TestContext(Square("b4"),Square("c3"),emptyPath= False, PartnerFigureInEndPos = False)
        ctx2.TurnColor = Color.BLACK
        ctx2.PrevPawn = Pawn(Color.WHITE)
        ctx2.PrevPawn.ConfirmMove()
        self.assertFalse(self.BlackPawn.isValideAttack(ctx2))

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suit = loader.loadTestsFromTestCase(TestPawn)
    runner = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0)
    result = runner.run(suit)
    if not result.wasSuccessful():
        msgs=[]
        if len(result.errors) > 0 :
            for test, traceback in result.errors:
                msgs.append(f'FAIL: {test.id()}')
        for test, traceback in result.failures:
            msgs.append(f'FAIL: {test.id()}')
        fullmsg= '\n\n'.join(msgs)
        raise AssertionError(fullmsg)