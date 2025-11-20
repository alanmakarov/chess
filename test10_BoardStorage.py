import unittest
import io
from Core.BoardStorage import BoardStorage
from Core.Color import Color
from Core.Square import Square
from Core.Interfaces import I_Figure, I_MovementContext
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
        self.board[Square("e3")] = MocFigure(Color.BLACK)
       

    def test_BoardClonned(self):
        clone_board = self.board.getClone()
        self.assertNotEqual(clone_board, self.board)

        clone_board[Square("e3")] = None
        self.assertNotEqual(clone_board[Square("e3")],self.board[Square("e3")])

        clone_board[Square("e2")] = MocFigure(Color.WHITE)
        self.assertNotEqual(clone_board[Square("e2")],self.board[Square("e2")])

    def test_figureCloned(self):
        clone_board = self.board.getClone()
        clone_board[Square("e2")].value = 2
       
        fg1 = clone_board[Square("e2")]
        fg2 = self.board[Square("e2")]
        self.assertNotEqual(fg1.value, fg2.value)

    def test_get(self):
        self.board.get_diag(Square("e1"),Square("e7"))

unittest.main()