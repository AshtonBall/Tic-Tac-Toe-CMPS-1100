import unittest
from unittest.mock import patch
import random

from TicTacToe2 import TicTacToe

class TestTicTacToe(unittest.TestCase):

    def make_game(self, size=3):
        game = TicTacToe.__new__(TicTacToe)
        game.size = size
        game.board = [" " for _ in range(size * size)]
        game.player = "X"
        game.computer = "O"
        return game
    
    def test_row_win(self):
        game = self.make_game(3)
        game.board = ["X", "X", "X",
                   " ", "O", " ",
                   " ", " ", "O"]
        self.assertTrue(game.checkWinner("X"))

    def test_computer_winning_move(self):
        game = self.make_game(3)
        game.board = ["O", "O", " ",
                   "X", "X", " ",
                   " ", " ", " "]
        game.computerMove()
        self.assertTrue(game.checkWinner("O"))

    def test_computer_block(self):
        game = self.make_game(3)
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


if __name__ == "__main__":
    unittest.main()