import unittest
import sys, os
sys.path.insert(
    0, 
    os.path.join(
        os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)), 'src'
    )
)
import mcts

class TestMcts(unittest.TestCase):
    def setUp(self):
        self.height = 6
        self.width = 7
        self.target = 4
        self.initial = ((),) * self.width        
        
        self.patient = mcts.ConnectFour(
            height=self.height, 
            width=self.width, 
            target=self.target
        )
    def test_p1_north_west_diagonal_win(self):
        """
        Regression test for the following situation were the player 1 win was 
        undetected:
        
        0 1 2 3 4 5 6 
        | | | | | | | |
        | | | |2| | | |
        |1| |2|1|2| | |
        |2|1|1|2|2| | |
        |1|2|1|2|1| | |
        |1|1|2|1|2| |1|
        """
        state = ((1, 1, 2, 1), (1, 2, 1), (2, 1, 1, 2), (1, 2, 2, 1, 2), (2, 1, 2, 2), (), (1,))
        self.assertEqual(self.patient.terminal(state), mcts.ConnectFour.VALUE_WIN)
        
if __name__ == '__main__':
    unittest.main()