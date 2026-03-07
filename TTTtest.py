import unittest
from unittest.mock import patch
import random
import io
from contextlib import redirect_stdout

from TicTacToe2 import TicTacToe, RED, BLUE, RESET

class TestTicTacToe(unittest.TestCase):

    def make_game(self, size=3, modes=None, k=None):
        game = TicTacToe.__new__(TicTacToe)
        game.size = size
        game.board = [" " for _ in range(size * size)]
        game.player = "X"
        game.computer = "O"
        game.modes = modes if modes is not None else ["classic"]
        game.k = k
        return game
    
    def test_row_win(self):
        game = self.make_game(3, modes=["classic"])
        game.board = ["X", "X", "X",
                   " ", "O", " ",
                   " ", " ", "O"]
        self.assertTrue(game.checkWinner("X"))

    def test_computer_winning_move(self):
        game = self.make_game(3, modes=["classic"])
        game.board = ["O", "O", " ",
                   "X", "X", " ",
                   " ", " ", " "]
        game.computerMove()
        self.assertTrue(game.checkWinner("O"))

    def test_computer_block(self):
        game = self.make_game(3, modes=["classic"])
        game.board = ["X", "X", " ",
                   "O", " ", " ",
                   " ", " ", "O"]
        game.computerMove()
        self.assertEqual(game.board[2], "O")  

    def test_board_reset_clears_board(self):
        game = self.make_game(4)
        game.board = ["X"] * 16
        game.boardReset()
        self.assertEqual(game.board, [" "] * 16)

    def test_forfeit_returns_forfeit(self):
        game = self.make_game(3)
        
        with patch("builtins.input", return_value="forfeit"):
            result = game.playerMove()
        self.assertEqual(result, "forfeit")

    def test_connectk_win(self):
        game = self.make_game(5, modes=["connectk"], k=4)
        game.board = ["X", "X", "X", "X", " ",
                      " ", " ", " ", " ", " ",
                      " ", " ", " ", " ", " ",
                      " ", " ", " ", " ", " ",
                      " ", " ", " ", " ", " "]
        self.assertTrue(game.checkWinner("X"))

    def test_square_win(self):
        game = self.make_game(4, modes=["square"])
        game.board = ["X", "X", " ", " ",
                      "X", "X", " ", " ",
                      " ", " ", " ", " ",
                      " ", " ", " ", " "]
        self.assertTrue(game.checkWinner("X"))

    def test_four_corners_win(self):
        game = self.make_game(4, modes=["corners"])
        game.board = ["O", " ", " ", "O",
                      " ", " ", " ", " ",
                      " ", " ", " ", " ",
                      "O", " ", " ", "O"]
        self.assertTrue(game.checkWinner("O"))

    def test_multiple_modes_win(self):
        game = self.make_game(4, modes=["classic", "square", "corners"])
        game.board = ["X", "X", " ", " ",
                      "X", "X", " ", " ",
                      " ", " ", " ", " ",
                      " ", " ", " ", " "]
        self.assertTrue(game.checkWinner("X"))

    def test_print_board_contains_colored_symbols(self):
        game = self.make_game(3)
        game.board = ["X", "O", " ",
                      " ", " ", " ",
                      " ", " ", " "]

        output = io.StringIO()
        with redirect_stdout(output):
            game.printBoard()

        printed = output.getvalue()
        self.assertIn(RED + "X" + RESET, printed)
        self.assertIn(BLUE + "O" + RESET, printed)


if __name__ == "__main__":
    unittest.main()