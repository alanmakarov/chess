import unittest
import io
from Core.BoardStorage import BoardStorage
from Core.Color import Color
from Core.Square import Square
from Core.Interfaces import I_Figure, I_MovementContext
from Figures.King import King
from Figures.Figure import Figure

class MocFigure(Figure):
    def __init__(self, color: Color):
        super().__init__(color)
        self.value = 1
    def isValideMove(self, ctx: I_MovementContext) -> bool:
        return True


class TestBoardStorage(unittest.TestCase):
    def setUp(self) -> None:
        self.board = BoardStorage()
        self.board[Square("e2")] = MocFigure(Color.BLACK)
        self.board[Square("e3")] = MocFigure(Color.WHITE)
        self.board[Square("d3")] = MocFigure(Color.WHITE)
        self.board[Square("b5")] = MocFigure(Color.BLACK)
       

    def test_BoardClonned(self):
        clone_board = self.board.getClone()
        self.assertNotEqual(clone_board, self.board)

        clone_board[Square("e3")] = None
        self.assertNotEqual(clone_board[Square("e3")],self.board[Square("e3")])

        clone_board[Square("e2")] = MocFigure(Color.WHITE)
        self.assertNotEqual(clone_board[Square("e2")],self.board[Square("e2")])

    # def test_figureCloned(self):
    #     clone_board = self.board.getClone()
    #     clone_board[Square("e2")].value = 2
       
    #     fg1 = clone_board[Square("e2")]
    #     fg2 = self.board[Square("e2")]
    #     self.assertNotEqual(fg1.value, fg2.value)

    def test_get_line(self):
        res = self.board.get_line(Square("e1"),Square("e7"))
        num = sum(1 for item in res if isinstance(item,I_Figure))
        num2 = sum(1 for item in res if isinstance(item,I_Figure) and item.Color == Color.WHITE)
        self.assertEqual(num,2)
        self.assertEqual(num2,1)

    def test_get_diag(self):
        res = self.board.get_diag(Square("f1"),Square("a6"))
        res2 = self.board.get_diag(Square("f1"),Square("c4"))
        num = sum(1 for item in res if isinstance(item,I_Figure))
        num2 = sum(1 for item in res2 if isinstance(item,I_Figure))
        self.assertEqual(num,3)
        self.assertEqual(num2,2)

    def test_get_kingSquare(self):
        self.board[Square("g5")] = King(Color.BLACK)
        self.board[Square("e1")] = King(Color.WHITE)

        res1 = self.board.get_king_square(Color.BLACK)
        res2 = self.board.get_king_square(Color.WHITE)
        self.assertEqual(res1,Square("g5"))
        self.assertEqual(res2,Square("e1"))

    def test_get_occupied_coordinates(self):
        self.board[Square("g5")] = MocFigure(Color.BLACK)
        res_black = self.board.get_occupied_coordinates(Color.BLACK)
        res_white = self.board.get_occupied_coordinates(Color.WHITE)
        self.assertEqual(len(res_black),3)
        self.assertEqual(len(res_white),2)


if __name__ == '__main__':
    loader = unittest.TestLoader()
    suit = loader.loadTestsFromTestCase(TestBoardStorage)
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