import unittest
import io
from Figures.Knight import Knight
from Figures.Figure import Figure
from Core.Interfaces import I_MovementContext
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

    
class TestKnight(unittest.TestCase):
    def setUp(self) -> None:
        self.BlackKnight = Knight(Color.BLACK)
        
    def test_KnightCorrectMove(self):
        ctx1 = TestContext(Square("b1"),Square("a3"))
        ctx2 = TestContext(Square("b1"),Square("c3"))
        ctx3 = TestContext(Square("b1"),Square("d2"))
        ctx4 = TestContext(Square("g1"),Square("e2"))

        ctx5 = TestContext(Square("a3"),Square("b1"))
        ctx6 = TestContext(Square("c3"),Square("b1"))
        ctx7 = TestContext(Square("d2"),Square("b1"))
        ctx8 = TestContext(Square("e2"),Square("g1"))

        self.assertTrue(self.BlackKnight.isValideMove(ctx1))
        self.assertTrue(self.BlackKnight.isValideMove(ctx2))
        self.assertTrue(self.BlackKnight.isValideMove(ctx3))
        self.assertTrue(self.BlackKnight.isValideMove(ctx4))
        self.assertTrue(self.BlackKnight.isValideMove(ctx5))
        self.assertTrue(self.BlackKnight.isValideMove(ctx6))
        self.assertTrue(self.BlackKnight.isValideMove(ctx7))
        self.assertTrue(self.BlackKnight.isValideMove(ctx8))

        attack_ctx = TestContext(Square("g6"),Square("f4"),emptyPath= False, PartnerFigureInEndPos = True)
        self.assertTrue(self.BlackKnight.isValideMove(attack_ctx)) 

    def test_KightIncorrectMove(self):
        ctx1 = TestContext(Square("b1"),Square("a2"))
        ctx2 = TestContext(Square("b1"),Square("b3"))
        ctx3 = TestContext(Square("b1"),Square("b2"))
        ctx4 = TestContext(Square("b1"),Square("d3"))

        self.assertFalse(self.BlackKnight.isValideMove(ctx1))
        self.assertFalse(self.BlackKnight.isValideMove(ctx2))
        self.assertFalse(self.BlackKnight.isValideMove(ctx3))
        self.assertFalse(self.BlackKnight.isValideMove(ctx4))

    def test_KnightAttack(self):
        attack_ctx = TestContext(Square("g6"),Square("f4"),emptyPath= False, PartnerFigureInEndPos = True)
        self.assertTrue(self.BlackKnight.isValideAttack(attack_ctx)) 
    

if __name__ == '__main__':
    loader = unittest.TestLoader()
    suit = loader.loadTestsFromTestCase(TestKnight)
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