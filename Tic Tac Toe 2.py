
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
                print("Invalid. Please enter and integer.")         # Requests valid input if input is not a number

        self.board = [" " for _ in range(self.size**2)]    # Stores board spaces for Tic Tac Toe symbols
        self.player = "X"           # Player is X
        self.computer = "O"         # Computer is O


    def printBoard(self):   # Displays the current state of the game board
        print()
        for row in range(self.size):                # Converting position to and index to insert onto board according to value of self.size
            for col in range(self.size):
                index = row * self.size + col
                print(self.board[index], end="")
                if col < self.size - 1:
                    print(" | ", end="")                        # Vertical line to separate cells
            if row < self.size - 1:
                print("\n" + "---" * (self.size ) + "--")       # Horizontal lines to separate cells
            else:
                print()
        print()

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
            move = input(f"Choose a position (1 - {max_spots}): ").strip()      # Prompts the player to choose a position using the board size
            if move.isdigit():
                index = int(move) - 1       # Convert to index
                if 0 <= index < max_spots and self.board[index] == " ":
                    self.board[index] = self.player
                    return

            print("Invalid move. try again.")       # Otherwise, the player must retry their move


    def play(self):                 # Starts the game
        print()
        print("Let's Play Tic Tac Toe!")
        print(f"Board: {self.size}x{self.size}")                                        # Introduction text
        print(f"You play as {self.player} and your oppnent plays as {self.computer}")
        print()
        print("Begin!")

        while True:                 
            self.printBoard()   
            self.playerMove()       # Player move

            if self.checkWinner(self.player):       # Checks if the player has won
                self.printBoard()
                print("You win!")
                break

            if self.boardFull():                    # Checks if the board is now full
                self.printBoard()
                print("It's a tie!")
                break

            self.computerMove()                     # Computer's turn to move
            print("Computer's move: ")
            self.printBoard()

            if self.checkWinner(self.computer):     # Checks if computer has won
                self.printBoard()
                print("Computer wins!")
                break

            if self.boardFull():                    # Checks if board is full again
                self.printBoard()
                print("It's a tie!")
                break


if __name__ == "__main__":              # Entry point and game start
    game = TicTacToe()
    game.play()