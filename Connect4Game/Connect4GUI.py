# Import necessary modules for creating a GUI and for displaying message boxes.
import tkinter as tk
from tkinter import messagebox
# import the Connect4Game file and name it as game for brevity.
import Connect4Game as game


class Connect4GUI:
    """
    This class creates a GUI for connect four including the game board, placing colored circles 
    in the boxes for each player, finding the winner, and displaying a message at the end of the game.
    
    Instance Variables
    ------------------
    self.master: (GUI window and parent widget.)
    
    self.master.title: (GUI screen title.)
    
    self.game: (object)
                 An instance of the Connect4Game class which computes the game logic.
                 
    self.buttons (list)
                  A list of tkinter buttons atop the game board displaying the column number. When clicked
                  the player's color is inserted in the bottom-most box of the column if the column has an
                  empty box.
                  
    self.canvas (tkinter widget)
                 Displays the game board with different colored circles for each player.
                 
    Methods
    -------
    
    make_move: Uses the logic from the make_move function on the Connect4Game file to determine if moves can
               be made and implements them. 
               Displays end of game message, and closes tkinter window without option for another game.
               
    draw_board: Draws the boxes for game board, inserts discs onto board to reflect the game state, and
                detremines weather the number boxes above board should be enabled or disabled
    
    
    """
    def __init__(self, master):
    # create a variable for the window of the GUI which will be the parent widget of all others
        self.master = master
    # title for the GUI screen
        self.master.title("Connect 4")
    # create an instance of the Connect4Game class from the game file
        self.game = game.Connect4Game()
        
    # list for column number buttons which will be above the game board.
    # A list of these buttons is necessary to be able to reference each one later in the program to know if
    # the functionality should be disabled if it's column is full
        self.buttons = []
        
    # loop seven times for amount of columns to add all buttons to the list
        for col in range(7):
    # these are the buttons with numbers on them. c is number of column that the make_move func takes and makes move in that column
    # the command of the button is a lambda function unique only to the buttons added during the loop
            button = tk.Button(master, text=str(col + 1), command=lambda c=col: self.make_move(c))
    # display on the same row but each one to the left of previous by using the next number of the loop
            button.grid(row=0, column=col)
    # append each button to button list
            self.buttons.append(button)
    # draw canvas seven units wide and 6 in height for seven columns of boxes and six rows
        self.canvas = tk.Canvas(master, width=7 * 60, height=6 * 60)
    # canvas is on row beneath the number buttons all the way to the left and spanning entire width of screen
        self.canvas.grid(row=1, column=0, columnspan=7)
    # call the function to draw the game board to show the board when app opens
        self.draw_board()

    def make_move(self, column):
        """
        This method tests if a column provided is valid for a game move, calls a function to draw the game board,
        displays a winning message, and ends the application.
        This method is called every time a number button is clicked.
        
        Parameters
        ----------
        column (int)
                The column number of the requested next move.
        """
    # call the make_move function from the Connect4Game file
        self.game.make_move(column)
    # call the draw_board function to redo the game board based on information gotten from the make_move function on 
    # the Connect4Game file
        self.draw_board()
    # check if self.winner on the Connect4Game file has a value for a winner
        if self.game.winner is not None:
    # get the value of self.winner and insert it into a wining message
            winner_text = f"Player {self.game.winner} wins!"
    # display message using messagebox module
            messagebox.showinfo("Game Over", winner_text)
    # close application when user clicks on msg box
            self.master.destroy()

    def draw_board(self):
        """
        This method draws the boxes for game board, inserts circles onto board to reflect the game state, and
        detremines weather the number boxes above board should be enabled or disabled.
        
        """
    # one way to keep the board synchronized with the game state is to clear it and repopulate if each move
        self.canvas.delete("all")
    # loop through all rows of board
        for row in range(6):
    # loop through all column to create a total of 42 boxes
            for col in range(7):
    # variables for the coordinates of each box. The first line represents the top left corner of each box
    # (keep in mind that in graphics the top left is (0, 0) as opposed to in mathematics) while the second 
    # line are for the bottom right corner which is always 60 more units away from the top left corner in 
    # both directions. This is accomplished by adding 60 to it on each iteration.
    # With each iteration of the col loop the boxes will move towards the right as the 
    # x0 icreases by 60, and with each iteration of the row loop the boxes will move downward by 60.
                x0, y0 = col * 60, row * 60
                x1, y1 = x0 + 60, y0 + 60
    # create a box with current values of coordinates based on current iteration of loops.
                self.canvas.create_rectangle(x0, y0, x1, y1, outline="black", fill="white")
                
    # accessing information from the board attribute of the Connect4Game class which holds all of the game moves
    # for each iteration of the loop assess the value of the box and display a circle if the box should have a value
                if self.game.board[row][col] == 1:
    # for player 1, create a red circle offset by 5 in both directions from the coordinates of the current box
                    self.canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill="red", outline="red")
    # same for player 2 but with yellow circle
                elif self.game.board[row][col] == 2:
                    self.canvas.create_oval(x0 + 5, y0 + 5, x1 - 5, y1 - 5, fill="yellow", outline="yellow")
                    
    # loop through all buttons with nums and check if top box in each colum is empty in order to know it button should be disabled 
        for col in range(7):
    # The test is done by using the iteration number as an index for the first sublist of self.board attribute 
    # from the Connect4Game file and chcecking if it is still empty.
            if self.game.board[0][col] == 0:
                self.buttons[col]["state"] = tk.NORMAL
            else:
    # if column is full disable the command from the button
                self.buttons[col]["state"] = tk.DISABLED


if __name__ == "__main__":
# variable for tkinter main window
    root = tk.Tk()
# pass that vaiable to the instance of the Connect4GUI class, which will function as self.master in the code
    app = Connect4GUI(root)
    root.mainloop()
