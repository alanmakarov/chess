import unittest
import io
from Figures.King import King
from Figures.Figure import Figure
from Core.Interfaces import I_MovementContext, I_Figure
from Core.Square import Square
from Core.Color import Color

class TestContext(I_MovementContext):
    def __init__(self, start: Square, end: Square, emptyPath = True, PartnerFigureInEndPos = False) -> None:
        self.start = start
        self.end = end
        self._passEmpty = emptyPath
        self._PartnerfigureInEndPos = PartnerFigureInEndPos

    def current_position(self) -> Square:
        return self.start
    def new_position(self) -> Square:
        return self.end
    def turnColor(self) -> Color:
        return Color.BLACK
    def isSquareEmpty(self, square) -> bool:
        return True
    def isPassEmpty(self) -> bool:
        return self._passEmpty
    def isNewPositionPartnerOccupied(self) -> bool:
        return self._PartnerfigureInEndPos
    def getFiguresOnPassAmmount(self) -> int:
        return 1 if self._PartnerfigureInEndPos else 0
    def getFigure(self, square: Square) -> I_Figure:
        return None
    def getPrevTurnFigure(self) -> I_Figure:
        return None
    def setEnPassantPawn(self, square: Square):
        pass
    
class TestKing(unittest.TestCase):
    def setUp(self) -> None:

        self.BlackKing = King(Color.BLACK)
        self.WhiteKing = King(Color.WHITE)
        
    def test_KingCorrectStandardMove(self):

        ctx1 = TestContext(Square("e1"),Square("f1")) # right 
        ctx2 = TestContext(Square("e1"),Square("d1")) # left 
        ctx3 = TestContext(Square("e1"),Square("e2")) # up
        ctx4 = TestContext(Square("e2"),Square("e1")) # down
        self.assertTrue(self.BlackKing.isValideMove(ctx1))
        self.assertTrue(self.BlackKing.isValideMove(ctx2))
        self.assertTrue(self.BlackKing.isValideMove(ctx3))
        self.assertTrue(self.BlackKing.isValideMove(ctx4))
        
        ctx1 = TestContext(Square("e1"),Square("f2")) # up right 
        ctx2 = TestContext(Square("e1"),Square("d2")) # up left
        self.assertTrue(self.BlackKing.isValideMove(ctx1))
        self.assertTrue(self.BlackKing.isValideMove(ctx2))
        ctx1 = TestContext(Square("e2"),Square("f1")) # down right 
        ctx2 = TestContext(Square("e2"),Square("d1")) # down left
        self.assertTrue(self.BlackKing.isValideMove(ctx1))
        self.assertTrue(self.BlackKing.isValideMove(ctx2))

    def test_KingIncorrectStandardMove(self):
        ctx1 = TestContext(Square("e1"),Square("e3")) 
        ctx2 = TestContext(Square("e1"),Square("g1"))
        ctx3 = TestContext(Square("e1"),Square("c1"))
        ctx4 = TestContext(Square("e3"),Square("e1"))
        self.assertFalse(self.BlackKing.isValideMove(ctx1))
        self.assertFalse(self.BlackKing.isValideMove(ctx2))
        self.assertFalse(self.BlackKing.isValideMove(ctx3))
        self.assertFalse(self.BlackKing.isValideMove(ctx4))

        ctx1 = TestContext(Square("e1"),Square("g3")) # up right 
        ctx2 = TestContext(Square("e1"),Square("b4")) # up left
        self.assertFalse(self.BlackKing.isValideMove(ctx1))
        self.assertFalse(self.BlackKing.isValideMove(ctx2))
        ctx1 = TestContext(Square("e3"),Square("g1")) # down right
        ctx2 = TestContext(Square("e3"),Square("c1")) # down left
        self.assertFalse(self.BlackKing.isValideMove(ctx1))
        self.assertFalse(self.BlackKing.isValideMove(ctx2))

        ctx1 = TestContext(Square("e1"),Square("e1")) # self move
        self.assertFalse(self.BlackKing.isValideMove(ctx1))
        
    def test_KingCorrectAttack(self):
        attack_ctx1 = TestContext(Square("e1"),Square("d2"),emptyPath= False, PartnerFigureInEndPos = True)
        attack_ctx2 = TestContext(Square("e1"),Square("e2"),emptyPath= False, PartnerFigureInEndPos = True)
        attack_ctx3 = TestContext(Square("e1"),Square("f2"),emptyPath= False, PartnerFigureInEndPos = True)
        self.assertTrue(self.BlackKing.isValideAttack(attack_ctx1))
        self.assertTrue(self.BlackKing.isValideAttack(attack_ctx2))
        self.assertTrue(self.BlackKing.isValideAttack(attack_ctx3))

    def test_KingIncorrectAttack(self):
        attack_ctx1 = TestContext(Square("e1"),Square("d2"),emptyPath= False, PartnerFigureInEndPos = False)
        attack_ctx2 = TestContext(Square("e1"),Square("e2"),emptyPath=True)
        self.assertFalse(self.BlackKing.isValideAttack(attack_ctx1))
        self.assertFalse(self.BlackKing.isValideAttack(attack_ctx2))




if __name__ == '__main__':
    loader = unittest.TestLoader()
    suit = loader.loadTestsFromTestCase(TestKing)
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