
import random               # implemented for when computer decoides to randomly choose a spot 



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


    def printBoard(self):   # Displays the current state of the game board
        print()

        num_cells = self.size * self.size
        cell_width = len(str(num_cells))           # Width must fit the largest number within the cell

        for row in range(self.size):                # Converting position to and index to insert onto board according to value of self.size
            for col in range(self.size):
                index = row * self.size + col

                if self.board[index] == " ":        # If the cell is empty, it will display a number corresponding to its cell number
                    value = str(index + 1)
                else:
                    value = self.board[index]

                print(value.rjust(cell_width), end="")

                if col < self.size - 1:
                    print(" | ", end="")                        # Vertical line to separate cells

            print()
            if row < self.size - 1:
                print("-" * ((cell_width + 3) * self.size - 3))       # Horizontal lines to separate cells
            else:
                print()
        print()

    def boardReset(self):
        self.board = [" " for _ in range(self.size * self.size)]

    def checkWinner(self, symbol):          # Checks to boards to see if player or computer has obtained a win condition
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
        print(f"Board: {self.size}x{self.size}")                                        # Introduction text
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
    game = TicTacToe()

    while True:
        game.boardReset()
        outcome = game.play()

        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("GAME ENDED")
            break
    