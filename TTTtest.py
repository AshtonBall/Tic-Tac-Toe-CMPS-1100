import unittest
import random
from TicTacToe2 import TicTacToe, GameSettings

class TestTicTacToe(unittest.TestCase):

    def setUp(self):
        """Set up a fresh game for each test"""
        settings = GameSettings()
        settings.size = 3
        settings.modes = ["classic"]
        self.game = TicTacToe(settings)

    # Tests the board
    def test_board_initialization(self):
        self.assertEqual(len(self.game.board), 9)
        self.assertEqual(self.game.board.count(" "), 9)
        self.assertEqual(self.game.player, "X")
        self.assertEqual(self.game.computer, "O")

    def test_valid_moves(self):
        self.assertEqual(len(self.game.validMoves()), 9)
        self.game.board[0] = "X"
        self.game.board[4] = "O"
        self.assertEqual(len(self.game.validMoves()), 7)

    def test_board_full(self):
        self.game.board = ["X"] * 9
        self.assertTrue(self.game.boardFull())
        self.game.board[0] = " "
        self.assertFalse(self.game.boardFull())

    # Tests for win conditions
    def test_classic_win_row(self):
        self.game.board = ["X", "X", "X", " ", " ", " ", " ", " ", " "]
        self.assertTrue(self.game.checkClassicWinner("X"))

    def test_classic_win_column(self):
        self.game.board = ["O", " ", " ", "O", " ", " ", "O", " ", " "]
        self.assertTrue(self.game.checkClassicWinner("O"))

    def test_classic_win_diagonal(self):
        self.game.board = ["X", " ", " ", " ", "X", " ", " ", " ", "X"]
        self.assertTrue(self.game.checkClassicWinner("X"))

    def test_check_winner_integrates_all_modes(self):
        settings = GameSettings()
        settings.modes = ["classic", "square"]
        game = TicTacToe(settings)
        
        # Test square win
        game.board = ["X", "X", " ", "X", "X", " ", " ", " ", " "]
        self.assertTrue(game.checkWinner("X"))

    def test_custom_win_pattern(self):
        settings = GameSettings()
        settings.modes = ["custom"]
        settings.custom_wins = [[0, 1, 2]]  # Top row
        game = TicTacToe(settings)
        
        game.board[0] = game.board[1] = game.board[2] = "X"
        self.assertTrue(game.checkWinner("X"))
        self.assertFalse(game.checkWinner("O"))

    # Tests for the AI TESTS
    def test_ai_easy_makes_move(self):
        settings = GameSettings()
        settings.difficulty = "easy"
        game = TicTacToe(settings)
        game.computerMove()
        self.assertEqual(game.board.count("O"), 1)

    def test_ai_medium_blocks_player(self):
        settings = GameSettings()
        settings.difficulty = "medium"
        game = TicTacToe(settings)
        
        # Give player almost a win
        game.board[0] = "X"
        game.board[1] = "X"
        game.computerMove()
        self.assertEqual(game.board[2], "O")  # Should block

    def test_ai_hard_finds_winning_move(self):
        settings = GameSettings()
        settings.difficulty = "hard"
        game = TicTacToe(settings)
        
        # Computer can win immediately
        game.board[0] = "O"
        game.board[1] = "O"
        game.computerMove()
        self.assertEqual(game.board[2], "O")

    # tests game flow
    def test_check_winner_after_move(self):
        self.game.board[0] = "X"
        self.game.board[1] = "X"
        self.game.board[2] = "X"
        self.assertTrue(self.game.checkWinner("X"))

    def test_custom_patterns_work_on_larger_boards(self):
        settings = GameSettings()
        settings.size = 4
        settings.modes = ["custom"]
        settings.custom_wins = [[0, 4, 8, 12]]  # First column on 4x4
        game = TicTacToe(settings)
        
        game.board[0] = game.board[4] = game.board[8] = game.board[12] = "X"
        self.assertTrue(game.checkWinner("X"))

    def test_connect_k_on_larger_board(self):
        settings = GameSettings()
        settings.size = 5
        settings.modes = ["connectk"]
        settings.k = 4
        game = TicTacToe(settings)
        
        # Create 4 in a row
        for i in range(4):
            game.board[i] = "X"
        self.assertTrue(game.checkWinner("X"))


if __name__ == '__main__':
    unittest.main(verbosity=2)