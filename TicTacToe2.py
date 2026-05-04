
import random               # implemented for when computer decoides to randomly choose a spot 
RED = "\033[91m"
BLUE = "\033[94m"           # Coloring for the symbols
RESET = "\033[0m"

class GameSettings:
    def __init__(self):                 # Default game settings
        self.size = 3
        self.modes = ["classic"]
        self.k = None
        self.difficulty = "medium"
        self.player_mode = "single"


def Rulebook():                                         # Displays the game rules for new players
    print("\n----- RULEBOOK -----")
    print("Classic: 3 in a row (or full board size win)")           # Defines the win conditions of each gamemode
    print("Connect-K: get K in a row in any direction")
    print("Square: make a 2x2 block")
    print("4 Corners: occupy all four corners")

    print("\nPlayer Modes:")                # Explains the different player modes
    print("- Single Player vs. Computer")
    print("- 2 Player local")

    print("\nControls:")                        # Explains the controls for the game
    print("- Enter a number to place a move")
    print("- Type 'forfeit' to quit a game")
    print("\n")
    input("Press Enter to return to menu...")       # Returns to main manu after thew rules screen
        
def settings_menu(settings):
    while True:                                         # Menu to alter game settings before starting a game
        print("\n----- SETTINGS -----")
        print(f"1. Board Size (current: {settings.size})")              # List of changable features
        print(f"2. Player Mode (current: {settings.player_mode})")
        print(f"3. Difficulty (current: {settings.difficulty})")
        print(f"4. Game Modes (current: {settings.modes})")
        print("5. Back")        # Goes back to main menu

        choice = input("Select: ").strip()      # Takes input to determine next action

        if choice == "1":                               # Pressing 1 opens the board size options
            size = input("Enter board size (3-10): ")
            if size.isdigit() and 3 <= int(size) <= 10:         # between 3 to 10 allowed
                settings.size = int(size)
                if settings.k and settings.k > settings.size:   # If board size is larger than the K value, it is reset
                    settings.k = None
                print("Updated board size.")        # Completeed action message

        elif choice == "2":                             # Pressing 2 aloows to choose between 1 or 2 players
            print("1: Single Player (vs Computer)")
            print("2: 2 Player Local")

            mode = input("Select: ")        # Selection for player mode 

            if mode == "1":
                settings.player_mode = "single"
            elif mode == "2":
                settings.player_mode = "two_player"

        elif choice == "3":                         # Pressing 3 allowing difficulty selection
            if settings.player_mode != "single":
                print("Difficulty disabled in 2-player mode.")      # Difficulty only for single player, so errormessage if changing in 2 player mode
                input("Press Enter to continue.")
                continue

            print("1: Easy  2: Medium  3: Hard")        # list of difficulties
            diff = input("Select difficulty: ")         # Select the difficulty
            if diff == "1":
                settings.difficulty = "easy"
            elif diff == "2":
                settings.difficulty = "medium"
            elif diff == "3":
                settings.difficulty = "hard"

        elif choice == "4":                         # Pressing 4 opens the game mode selection menu
            print("Choose modes (e.g. 1 2 3):")
            print("1 Classic")
            print("2 Connect-K")
            print("3 Square")
            print("4 4 Corners")

            choice_modes = input("> ").split()      # Takes input of chosen mode; must be 1, 2, 3, or 4
            valid = {"1", "2", "3", "4"}

            if any(m not in valid for m in choice_modes):       # If anything other than valid selection, an error message is displayed
                print("Invalid modes.")
                continue

            settings.modes = []     # List of applied modes

            if "1" in choice_modes:                     # Adds selected modes to the modes list
                settings.modes.append("classic")
            if "2" in choice_modes:
                settings.modes.append("connectk")
            if "3" in choice_modes:
                settings.modes.append("square")
            if "4" in choice_modes:
                settings.modes.append("corners")

            if "connectk" in settings.modes:            # For connect-k, a k value must be chosen
                while True:
                    k = input(f"Enter K value (2-{settings.size}): ").strip()
                    if k.isdigit():
                        k_val = int(k)
                        if 2 <= k_val <= settings.size:
                            settings.k = k_val
                            break
                        else:
                            print(f"K must be between 2 and {settings.size}!")  # K cannot be larger than board size
                    else:
                        print("Please enter a number.")

        elif choice == "5":     # Back to main menu
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

        self.turn = "X"     # used in two palyer mode


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

    def checkWinner(self, symbol):  # Calls the appropriate checkWinner function for the chosen gamemodes; Checks for win condition
        
        for mode in self.modes:                                                 # Lops through gamemodes and checks if any win condition is met
            if mode == "classic" and self.checkClassicWinner(symbol):
                return True
            elif mode == "connectk" and self.checkConnectKWinner(symbol):
                return True
            elif mode == "square" and self.checkSquareWinner(symbol):
                return True
            elif mode == "corners" and self.checkCornersWinner(symbol):
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
        if "connectk" not in self.modes or self.k is None:      # Skips if connect-k mode not in use
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
    

    def computerMove(self):                 # Determines the computer's difficulty mode to call appropriate function
        if self.difficulty == "easy":
            self.AI_easy()
        elif self.difficulty == "medium":
            self.AI_medium()
        elif self.difficulty == "hard":
            self.AI_hard()


    def AI_easy(self):      # Easy AI just mades random moves without strategy
        """Random move"""   
        self.board[random.choice(self.validMoves())] = self.computer


    def AI_medium(self):                # Medium AI tries to win, blocks if player almost wins, and chooses randomly otherwise
        # Try to win
        for index in self.validMoves():
            self.board[index] = self.computer
            if self.checkWinner(self.computer): # If the next move is a win, it takes it
                return
            self.board[index] = " "

        # Block player
        for index in self.validMoves():
            self.board[index] = self.player
            if self.checkWinner(self.player):           # If the player is clsoe to a win, the computer takes the spot to block the player
                self.board[index] = self.computer
                return
            self.board[index] = " "

        self.AI_easy()      # Implements random move if no other good option is found


    def AI_hard(self):         # algorithm that chooses the best move by looking at future possible moves   
        best_score = -float('inf')  
        best_move = None

        for index in self.validMoves():
            self.board[index] = self.computer
            score = self.minimax(False)     # alrogrithm evauluates the move by looking at future moves and assigns a score to the move
            self.board[index] = " "

            if score > best_score:      # chooses the move with the best score
                best_score = score
                best_move = index

        if best_move is not None:               # If there is a valid move, the computer takes it
            self.board[best_move] = self.computer


    def minimax(self, is_maximizing):       # alrgorithm for looking at future moves and assigning scores to them
        """Minimax algorithm"""
        if self.checkWinner(self.computer):     # Positive score for computer win
            return 10
        if self.checkWinner(self.player):       # Negative score for player win
            return -10
        if self.boardFull():                    # Neutral score for tie or no win condition
            return 0

        if is_maximizing:   # Computer's turn
            best_score = -float('inf')          
            for index in self.validMoves():         # Loops through valid moves and recursively calls minimax to choose move with highest score
                self.board[index] = self.computer   
                score = self.minimax(False)
                self.board[index] = " "
                best_score = max(score, best_score)
            return best_score
        else:               # Player's turn
            best_score = float('inf')
            for index in self.validMoves():         # Loops through valid moves and recursively calls minimax to choose move with lowest score for the player
                self.board[index] = self.player
                score = self.minimax(True)
                self.board[index] = " "
                best_score = min(score, best_score)
            return best_score


    def playerMove(self):                   # Used to allow the player to choose a move
        while True:
            move = input("Choose a position or 'forfeit': ").lower()        # Takes player input for move or forfeit

            if move == "forfeit":       # Player can forfeit
                return "forfeit"

            if move.isdigit():          # If the move is a number, it checks it validity
                i = int(move) - 1
                if 0 <= i < len(self.board) and self.board[i] == " ":
                    self.board[i] = self.player     # If valid, the move is complete
                    return None

            print("Invalid move.")      # If invalid, an error message is dsiplayed


    def play(self):                 # Starts the game
        print()
        print("Let's Play Tic Tac Toe!")            # Setup text that is displayed before each game
        print(f"Board: {self.size}x{self.size}")  
        print(f"Gamemodes: {self.modeNames()}")
        if self.player_mode == "single":                # only displays difficulty in single player mode
            print(f"Difficulty: {self.difficulty}")
        print()
        if "connectk" in self.modes:                    # only displays K value if connect-k is used
            print(f"Get {self.k} in a row to win!")
                                              # Introduction text
        print(f"You play as {self.player} and your opponent plays as {self.computer}")      # Explains the symbols
        print("If you wish to quit the game early, type 'forfeit'")
        print()
        print("Begin!")     # Game starts

        while True:             # Main game loop that continues until win, loss, tie, or forfeit
            self.printBoard()

            if self.player_mode == "two_player":        # Sets two=player mode if selected in settings


                # Two Player mode
                move = input(f"Player {self.turn}, choose a position (or 'forfeit'): ").lower()     # Player input for move

                if move == "forfeit":
                    print(f"Player {self.turn} forfeits!")
                    return

                if move.isdigit():          # if the move is a number, its validity is checked
                    i = int(move) - 1
                    if 0 <= i < len(self.board) and self.board[i] == " ":
                        self.board[i] = self.turn

                        if self.checkWinner(self.turn):             # Looks for a win condition after each move
                            self.printBoard()
                            print(f"Player {self.turn} Wins!")
                            return

                        if self.boardFull():                        # looks for a full board for tie
                            self.printBoard()
                            print("Tie!")
                            return

                        self.turn = "O" if self.turn == "X" else "X"            # Switches playign symbol for X and O after each turn
                    else:
                        print("Invalid move!")
                else:                                       # Error messages for invalid inputs
                    print("Please enter a number.")

            
            else:
                # Single Player mode
                result = self.playerMove()  
                if result == "forfeit":             # Forfeit option for single player
                    print("You forfeited!")
                    return

                if self.checkWinner(self.player):       # Checks for player win after move
                    self.printBoard()
                    print("You win!")
                    return "player"

                if self.boardFull():        # Checks for tie after player move
                    self.printBoard()
                    print("Tie!")
                    return "tie"

                self.computerMove()     # Computer decides its move (used the chosen difficulty)

                if self.checkWinner(self.computer):     # Checks for a computer win after each move
                    self.printBoard()
                    print("Computer wins!")
                    return

                if self.boardFull():        # Checks for a tie after computer move
                    self.printBoard()
                    print("Tie!")
                    return "tie"
            


def start_game(settings):       # Function that asks if the player wants to play again or change settings after each game
    while True:
        game = TicTacToe(settings)
        game.play()

        choice = input("\nPlay again with same settings? (y/n): ").strip().lower()

        if choice != "y":
            break


def mainMenu():                 # Main menu loop that allows player to change game settings, view rules, start game, or quit game
    settings = GameSettings()

    while True:
        print("\n----- MAIN MENU -----")        # Main menu display
        print("1. Start Game")
        print("2. Settings")
        print("3. Rules")
        print("4. Quit")

        choice = input("> ")            # Inpput for main menu selection

        if choice == "1":           # Starts game with applied settings
            start_game(settings)

        elif choice == "2":             # opens settings menu
            settings_menu(settings)

        elif choice == "3":         # Displays the game's rules
            Rulebook()

        elif choice == "4":         # Quits the game loop and ends the program
            print("Goodbye!")
            break

        else:                       # Error message
            print("Invalid choice")


if __name__ == "__main__":      # Starts program by calling main menu function as a start point
    mainMenu()