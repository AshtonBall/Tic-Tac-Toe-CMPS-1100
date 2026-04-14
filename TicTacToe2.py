
import random               # implemented for when computer decoides to randomly choose a spot 
RED = "\033[91m"
BLUE = "\033[94m"           # Coloring for the symbols
RESET = "\033[0m"

class GameSettings:
    def __init__(self):
        self.size = 3
        self.modes = ["classic"]
        self.k = None
        self.difficulty = "medium"
        self.player_mode = "single"


def Rulebook():
    print("\n----- RULEBOOK -----")
    print("Classic: 3 in a row (or full board size win)")
    print("Connect-K: get K in a row in any direction")
    print("Square: make a 2x2 block")
    print("4 Corners: occupy all four corners")

    print("\nPlayer Modes:")
    print("- Single Player vs. Computer")
    print("- 2 Player local")

    print("\nControls:")
    print("- Enter a number to place a move")
    print("- Type 'forfeit' to quit a game")
    print("\n")
    input("Press Enter to return to menu...")
        
def settings_menu(settings):
    while True:
        print("\n----- SETTINGS -----")
        print(f"1. Board Size (current: {settings.size})")
        print(f"2. Player Mode (current: {settings.player_mode})")
        print(f"3. Difficulty (current: {settings.difficulty})")
        print(f"4. Game Modes (current: {settings.modes})")
        print("5. Back")

        choice = input("Select: ").strip()

        if choice == "1":
            size = input("Enter board size (3-10): ")
            if size.isdigit() and 3 <= int(size) <= 10:
                settings.size = int(size)
                print("Updated board size.")

        elif choice == "2":
            print("1: Single Player (vs Computer)")
            print("2: 2 Player Local")

            mode = input("Select: ")

            if mode == "1":
                settings.player_mode = "single"
            elif mode == "2":
                settings.player_mode = "two_player"

        elif choice == "3":
            if settings.player_mode != "single":
                print("Difficulty disabled in 2-player mode.")
                continue

            print("1: Easy  2: Medium  3: Hard")
            diff = input("Select difficulty: ")
            if diff == "1":
                settings.difficulty = "easy"
            elif diff == "2":
                settings.difficulty = "medium"
            elif diff == "3":
                settings.difficulty = "hard"

        elif choice == "4":
            print("Choose modes (e.g. 1 2 3):")
            print("1 Classic")
            print("2 Connect-K")
            print("3 Square")
            print("4 4 Corners")

            choice_modes = input("> ").split()
            valid = {"1", "2", "3", "4"}

            if any(m not in valid for m in choice_modes):
                print("Invalid modes.")
                continue

            settings.modes = []

            if "1" in choice_modes:
                settings.modes.append("classic")
            if "2" in choice_modes:
                settings.modes.append("connectk")
            if "3" in choice_modes:
                settings.modes.append("square")
            if "4" in choice_modes:
                settings.modes.append("corners")

            if "2" in choice_modes:
                k = input("Enter K value: ")
                if k.isdigit():
                    settings.k = int(k)

        elif choice == "5":
            return


class TicTacToe:            # Tic Tac Toe game implemented as a class. The board size will be chosen by the player. More features will be added

    def __init__(self, settings):     # Initializes the class
        self.size = settings.size
        self.board = [" " for _ in range(self.size**2)]
        self.player = "X"
        self.computer = "O"

        self.modes = settings.modes
        self.k = settings.k
        self.difficulty = settings.difficulty
        self.player_mode = settings.player_mode

        self.turn = "X"


    def modeNames(self):
        names = []      #empty list to append used modes to

        for mode in self.modes:     # Appends the appropriate gamemodes to the names list based on which were chosen           
            if mode == "classic":
                names.append("Classic")
            elif mode == "connectk":
                names.append(f"Connect-{self.k}")
            elif mode == "square":
                names.append("Square")
            elif mode == "corners":
                names.append("4 Corners")

        return ", ".join(names)     # joins them using commas

    def printBoard(self):   # Displays the current state of the game board
        print()

        num_cells = self.size * self.size
        cell_width = len(str(num_cells))           # Width must fit the largest number within the cell

        for row in range(self.size):                # Converting position to and index to insert onto board according to value of self.size
            for col in range(self.size):
                index = row * self.size + col

                if self.board[index] == " ":                        # If the cell is empty, it will display a number corresponding to its cell number
                    value = str(index + 1).rjust(cell_width)
                elif self.board[index] == "X":
                    value = " " * (cell_width - 1) + RED + "X" + RESET
                elif self.board[index] == "O":                          # Now, the inserted symbols are colored for clarity
                    value = " " * (cell_width - 1) + BLUE + "O" + RESET
                    

                print(value, end="")

                if col < self.size - 1:
                    print(" | ", end="")                        # Vertical line to separate cells

            print()
            if row < self.size - 1:
                print("-" * ((cell_width + 3) * self.size - 3))       # Horizontal lines to separate cells
            else:
                print()
        print()

    def boardReset(self):
        self.board = [" " for _ in range(self.size * self.size)]        # Wipes the board

    def checkWinner(self, symbol):                                          # Calls the appropriate checkWinner function for the chosen gamemode
        return (
            self.checkClassicWinner(symbol)
            or self.checkConnectKWinner(symbol)
            or self.checkSquareWinner(symbol)
            or self.checkCornersWinner(symbol)
        )

    def checkClassicWinner(self, symbol):          # Checks to boards to see if player or computer has obtained a win condition
        s = self.size

        for row in range(s):                                                        # Check rows for win condition
            if all(self.board[row * s + col] == symbol for col in range(s)):
                return True
            
        for col in range(s):                                                        # Check columns for win condition
            if all(self.board[row * s + col] == symbol for row in range(s)):
                return True
        
        if all (self.board[i * s + i] == symbol for i in range(s)):                 # Checks diagonal from top-left to bottom-right
            return True
        
        if all(self.board[i * s + (s - 1 - i)] == symbol for i in range(s)):        # Checks diagonal from top-right to bottom-left
            return True
        
        return False        # No win condition met
    
    def checkConnectKWinner(self, symbol):      # Connect-K gamemode win condtion
        if "connectk" not in self.modes:
            return False
        
        s = self.size       # size of board
        k = self.k          # number in row needed for win

        
        for row in range(s):            # Checks rows for the appropriate length of same symbols
            for col in range(s - k + 1):
                if all(self.board[row * s + (col + i)] == symbol for i in range(k)):
                    return True

        for row in range(s - k + 1):    # Checks columns for the appropriate length of same symbols
            for col in range(s):
                if all(self.board[(row + i) * s + col] == symbol for i in range(k)):
                    return True

        for row in range(s - k + 1):    # Checks diagonal down-right for the appropriate length of same symbols
            for col in range(s - k + 1):
                if all(self.board[(row + i) * s + (col + i)] == symbol for i in range(k)):
                    return True

        for row in range(s - k + 1):    # Checks diagonal down-left for the appropriate length of same symbols
            for col in range(k - 1, s):
                if all(self.board[(row + i) * s + (col - i)] == symbol for i in range(k)):
                    return True

        return False        # No win condition found

    def checkSquareWinner(self, symbol):
        if "square" not in self.modes:
            return False
        s = self.size   # size of board

        for row in range(s - 1):            # loops to check every 2x2 square
            for col in range(s - 1):

                top_left = row * s + col            # converts row and column positions to board indexes
                top_right = row * s + col + 1
                bottom_left = (row + 1) * s + col
                bottom_right = (row + 1) * s + col + 1

                if (                                        # checks if all four spaces in a square have the same symbol
                    self.board[top_left] == symbol and
                    self.board[top_right] == symbol and
                    self.board[bottom_left] == symbol and
                    self.board[bottom_right] == symbol
                ):
                    return True             # Square formed

        return False            # No square formed

    def checkCornersWinner(self, symbol):
        if "corners" not in self.modes:
            return False
        
        s = self.size                                           # size of board
        corners = [0, s - 1, s * (s - 1), s * s - 1]            # indexes of the four corners of the board
        return all(self.board[i] == symbol for i in corners)    # checks if all corners have the same symbol

    def boardFull(self):                # Determines if there are no more empty cells on the board
        return " " not in self.board
    
    
    def validMoves(self):               # Creates a list of indexes that are still available for the computer
        return [i for i in range(len(self.board)) if self.board[i] == " "]
    

    def computerMove(self):             

        if self.difficulty == "easy":
            self.AI_easy()

        elif self.difficulty == "medium":
            self.AI_medium()

        elif self.difficulty == "hard":
            self.AI_hard()


    # AI choices
    def AI_easy(self):
        self.board[random.choice(self.validMoves())] = self.computer


    def AI_medium(self):

        # try win
        for index in self.validMoves():
            self.board[index] = self.computer
            if self.checkWinner(self.computer):
                return
            self.board[index] = " "

        # block player
        for index in self.validMoves():
            self.board[index] = self.player
            if self.checkWinner(self.player):
                self.board[index] = self.computer
                return
            self.board[index] = " "

        # random
        self.AI_easy()


    def AI_hard(self):

        # 1. win
        for index in self.validMoves():
            self.board[index] = self.computer
            if self.checkWinner(self.computer):
                return
            self.board[index] = " "

        # 2. block
        for index in self.validMoves():
            self.board[index] = self.player
            if self.checkWinner(self.player):
                self.board[index] = self.computer
                return
            self.board[index] = " "

        # 3. center
        center = (self.size * self.size) // 2
        if self.board[center] == " ":
            self.board[center] = self.computer
            return
        
         # 4. take first available corner (NEW IMPROVEMENT)
        corners = [0, self.size - 1, self.size * (self.size-1), self.size * self.size - 1]
        for c in corners:
            if self.board[c] == " ":
                self.board[c] = self.computer
                return

        # 5. random
        self.AI_easy()


    def playerMove(self):                   # Used to allow the player to choose a move
        while True:
            move = input("Choose a position or 'forfeit': ").lower()

            if move == "forfeit":
                return "forfeit"

            if move.isdigit():
                i = int(move) - 1
                if 0 <= i < len(self.board) and self.board[i] == " ":
                    self.board[i] = self.player
                    return None

            print("Invalid move.")


    def play(self):                 # Starts the game
        print()
        print("Let's Play Tic Tac Toe!")
        print(f"Board: {self.size}x{self.size}")  
        print(f"Gamemodes: {self.modeNames()}")
        if self.player_mode == "single":
            print(f"Difficulty: {self.difficulty}")
        print()
        if "connectk" in self.modes:
            print(f"Get {self.k} in a row to win!")
                                              # Introduction text
        print(f"You play as {self.player} and your opponent plays as {self.computer}")
        print("If you wish to quit the game early, type 'forfeit'")
        print()
        print("Begin!")

        while True:
            self.printBoard()

            if self.player_mode == "two_player":

                move = input(f"Player {self.turn}, choose a position (or 'forfeit'): ").lower()

                if move == "forfeit":
                    print(f"Player {self.turn} forfeits!")
                    return

                if move.isdigit():
                    i = int(move) - 1
                    if 0 <= i < len(self.board) and self.board[i] == " ":
                        self.board[i] = self.turn
                    else:
                        print("Invalid move.")
                        continue
                else:
                    print("Invalid move.")
                    continue

                if self.checkWinner(self.turn):
                    self.printBoard()
                    print(f"Player {self.turn} wins!")
                    return

                if self.boardFull():
                    self.printBoard()
                    print("Tie!")
                    return

                self.turn = "O" if self.turn == "X" else "X"
            
            else:
                result = self.playerMove()
                if result == "forfeit":
                    print("You forfeited!")
                    return

                if self.checkWinner(self.player):
                    self.printBoard()
                    print("You win!")
                    return "player"

                if self.boardFull():
                    self.printBoard()
                    print("Tie!")
                    return "tie"

                self.computerMove()

                if self.checkWinner(self.computer):
                    self.printBoard()
                    print("Computer wins!")
                    return

                if self.boardFull():
                    self.printBoard()
                    print("Tie!")
                    return "tie"
            


def start_game(settings):
    while True:
        game = TicTacToe(settings)
        game.play()

        choice = input("\nPlay again with same settings? (y/n): ").strip().lower()

        if choice != "y":
            break


def mainMenu():
    settings = GameSettings()

    while True:
        print("\n----- MAIN MENU -----")
        print("1. Start Game")
        print("2. Settings")
        print("3. Rules")
        print("4. Quit")

        choice = input("> ")

        if choice == "1":
            start_game(settings)

        elif choice == "2":
            settings_menu(settings)

        elif choice == "3":
            Rulebook()

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice")


if __name__ == "__main__":
    mainMenu()