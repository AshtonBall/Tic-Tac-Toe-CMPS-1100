
import random               # implemented for when computer decoides to randomly choose a spot 
RED = "\033[91m"
BLUE = "\033[94m"           # Coloring for the symbols
RESET = "\033[0m"


class TicTacToe:            # Tic Tac Toe game implemented as a class. The board size will be chosen by the player. More features will be added

    def __init__(self):     # Initializes the class
        while True:
            try:
                size = int(input("Choose the size of your Tic tac Toe board: "))        # Player decides board size
                if size >= 3 and size <= 10:                   # The board cannot be smaller than 3x3 units or bigger than 10x10 units
                    self.size = size        
                    break                       # Leaves while loop if valid size
                else:
                    print("Board size must be between 3 and 10.")       # Requests valid input if a number less than 3 or greater than 10 is chosen
            except ValueError:
                print("Invalid. Please enter an integer.")         # Requests valid input if input is not a number

        self.board = [" " for _ in range(self.size**2)]    # Stores board spaces for Tic Tac Toe symbols
        self.player = "X"           # Player is X
        self.computer = "O"         # Computer is O

        self.modes = []         # Initializes with an empty lsit of applied gamemodes
        self.k = None           # Variable for the number in a row needed specifically in Connect-K mode
        self.chooseModes()      # Prompts the player to choose mode

    def chooseModes(self):
        while True:
            print()
            print("Choose one or more game modes:")         # Displays the gamemode choices
            print("1: Classic")
            print("2: Connect-K")
            print("3: Square")
            print("4: 4 Corners")

            choice = input("Select your game modes (1-4): ").replace(",", " ").split()      # 4 gamemodes, can be typed with spaces or commas between numbers

            valid = {"1", "2", "3", "4"}    # valid inputs to choose a gamemode

            if not choice:                                  # Shown is nothing is typed      
                print("Please choose at least one mode")
                continue

            if any(item not in valid for item in choice):   # Shown if input does not match the valid inputs
                print("Invalid choice. Try again.")
                continue

            choice = list(dict.fromkeys(choice))              # removes duplicates in player's input for chosen modes

            self.modes = []     # Creates a list of chosen game modes

            if "1" in choice:                   # Each appends the corresponding gamemode to thew list of chosen modes
                self.modes.append("classic")        
            if "2" in choice:
                self.modes.append("connectk")
            if "3" in choice:
                self.modes.append("square")
            if "4" in choice:
                self.modes.append("corners")

            if "2" in choice:           # Extra output required for Connect-K game mode
                while True:
                    try:
                        k = int(input(f"How many in a row will you need to win? (3-{self.size}): "))       # User chooses how many in a row are needed in Connect-K game mode
                        if 3 <= k <= self.size:     # Must be between 3 and the selected board size
                            self.k = k          # This is the variable for how many must be in a row for a win
                            break
                        else:
                            print(f"Please choose a number 3-{self.size}.")     # If input is out of allowed range
                    except ValueError:
                        print("Please enter a whole number.")       # If input is not an integer
                break
            else:
                self.k = None

            break

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
        if "classic" in self.modes and self.checkClassicWinner(symbol):
            return True

        if "connectk" in self.modes and self.checkConnectKWinner(symbol):
            return True

        if "square" in self.modes and self.checkSquareWinner(symbol):
            return True

        if "corners" in self.modes and self.checkCornersWinner(symbol):
            return True

        return False

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
        s = self.size                                           # size of board
        corners = [0, s - 1, s * (s - 1), s * s - 1]            # indexes of the four corners of the board
        return all(self.board[i] == symbol for i in corners)    # checks if all corners have the same symbol

    def boardFull(self):                # Determines if there are no more empty cells on the board
        return " " not in self.board
    
    
    def validMoves(self):               # Creates a list of indexes that are still available for the computer
        s = self.size
        return [i for i in range(s * s) if self.board[i] == " "]
    

    def computerMove(self):             # Simple and base computer behavior in a game

        for i in self.validMoves():             # Checks for cells to enter for a win
            self.board[i] = self.computer
            if self.checkWinner(self.computer):
                return
            self.board[i] = " "

        for i in self.validMoves():             # Computer tries to place symbol in the way of the player to prevent a win
            self.board[i] = self.player
            if self.checkWinner(self.player):
                self.board[i] = self.computer
                return
            self.board[i] = " "

        i = random.choice(self.validMoves())     # Chooses a random move if neither other condition is needed
        self.board[i] = self.computer


    def playerMove(self):                   # Used to allow the player to choose a move
        max_spots = self.size**2
        while True:
            move = input(f"Choose a position (1 - {max_spots}) or type 'forfeit' to give up: ").strip().lower()      # Prompts the player to choose a position using the board size OR choose the preenptively end the game if they wish

            if move == "forfeit":
                return "forfeit"

            if move.isdigit():
                index = int(move) - 1       # Convert to index
                if 0 <= index < max_spots and self.board[index] == " ":
                    self.board[index] = self.player
                    return None

            print("Invalid move. try again.")       # Otherwise, the player must retry their move


    def play(self):                 # Starts the game
        print()
        print("Let's Play Tic Tac Toe!")
        print(f"Board: {self.size}x{self.size}")  
        print(f"Gamemodes: {self.modeNames()}")
        if "connectk" in self.modes:
            print(f"Get {self.k} in a row to win!")
                                              # Introduction text
        print(f"You play as {self.player} and your opponent plays as {self.computer}")
        print("If you wish to quit the game early, type 'forfeit'")
        print()
        print("Begin!")

        while True:                 
            self.printBoard()   
            result = self.playerMove()       # Player move

            if result == "forfeit":
                self.printBoard()
                print("You forfeited. Computer wins!")
                return "forfeit"

            if self.checkWinner(self.player):       # Checks if the player has won
                self.printBoard()
                print("You win!")
                return "player"

            if self.boardFull():                    # Checks if the board is now full
                self.printBoard()
                print("It's a tie!")
                return "tie"

            self.computerMove()                     # Computer's turn to move
            print("Computer's move: ")
            self.printBoard()

            if self.checkWinner(self.computer):     # Checks if computer has won
                print("Computer wins!")
                return "computer"

            if self.boardFull():                    # Checks if board is full again3
                print("It's a tie!")
                return "tie"


if __name__ == "__main__":              # Entry point and game start
    while True:
        game = TicTacToe()
        outcome = game.play()

        again = input("Play again? (y/n): ").strip().lower()        # Player types y or n to start a new game
        if again != "y":
            print("GAME ENDED")
            break
    

    # game restarts and user chooses game modes and board size again