# Importing the module that creates abstract classes. These classes cannot be implemented since they have no 
# commands but they will be implemented by a class that inherits them and defines its methods 
# with real commands. These classes are useful as they can be thought of as a bluepring for classes that inherit
# from them which must contain code to properly define these methods.
from abc import (ABC, abstractmethod)


class Connect4GameStrategy(ABC):
    def __init__(self):
        ...
# this decorator indicates that this function is now useless but will be properly defined by a subclass.
    @abstractmethod
    def strategy(self, game_safety_copy):
        ...
        """
        Abstract method for the game strategy
        
        Parameters
        ----------
        game_safety_copy:
          A safe copy of the game to work on without tampering and possibly runing the real game data.
          
        """

class Connect4Game:
    """
    This class creates a game board for connect four, tests if moves are valid before moves are made, and 
    checks for a winner by looking for four consecutive identical values in vertical, horizontal, and diagnol
    directions.
    
    Instance Variables
    ------------------
    self.board: (Nested list)
                 Game board of six rows and seven columns
    self.current_player (int)
                 An integer representing each of the players
    self.winner (None or int)
                 Variable initialized to None and changed to player's number if player wins.
                 
    Methods
    -------
    is_valid_move: Checks if move is valid or not
    
    make_move: iterates through column to find first empty spot, checks for winner after each move,
               and switches self.player to next player.
               
    check_for_winner: Evaluates a game state for game-winning patterns.
    
    check_line: Checks for similar values in a vertical, horizontal, or diagnol line.
    
    """
    def __init__(self):
        # create game board as nested sublist. Game will have six rows and seven columns
        self.board = [[0] * 7 for _ in range(6)]
        # set a specific player to go first, using number 1 as identifier
        self.current_player = 1
        # start off game with no winner yet
        self.winner = None

    def is_valid_move(self, column):
        """
        This method tests if a column provided is valid for a game move.
        
        Parameters
        ----------
        column (int)
                The column number of the requested next move.
                
        Returns
        -------
        bool: False if column is out of bounds or if move cannot be done in column provided, 
              and True if move is valid.
        """
        # check if column is valid  number. Since there are seven values in each sublist representing each column,
        # the number must be less than seven and greater than or equal to zero reflecting the index range of the sublists.
        if not (0 <= column < 7):
        # return false for an invalid move
            return False
        # when column number is in appropriate range, return a boolean of true if the index of column in the first sublist is equal
        # to zero which means that it is still unoccupied. This sublist is the top row of the game board so if the index of [0][column] 
        # is equal to zero that column isn't full and can be used for moves. Returns false if the top row of index isn't equal zero.
        return self.board[0][column] == 0

    def make_move(self, column):
        """
        This method continues the work of the previous function and after more rigorous testing makes implements a move.
        
        Parameters
        ----------
        column (int)
                The column number of the requested next move.
                
        Returns
        -------
        Nothing, when move isn't valid because of winner, full column or because move has been made and funciton finishes.
        """
        # test if move is valid with previous function or if there is already a winner.
        if not self.is_valid_move(column) or self.winner is not None:
        # quit function since move cannot be made due to finding winner or non valid column
            return
        # otherwise meaning the column is valid and there is no winner yet
        # loop through the rows of the provided column. Start from bottom of board which is index of five and decrese by one
        # and go through zero which is top row. If no empty index is found in first round, loop will iterate until it finds
        # empty index. We are guaranteed to find an empty index since is_valid_move returned True
        for row in range(5, -1, -1):
        # if bottom-most row is empty
            if self.board[row][column] == 0:
        # enter value of current player in that index as a move in the game
                self.board[row][column] = self.current_player
        # call check_winner function to check if the current move produces a win for current player
                if self.check_winner(row, column):
        # if it does declare current player as winner
                    self.winner = self.current_player
        # if game is still without a winner
                else:
        # continue game and set self.current player to opponent. The number will be a 2. If opponent is moving the number will be one
                    self.current_player = 3 - self.current_player
        # once move was made and player switched to opponent the function ends
                return

    def check_winner(self, row, col):
        """
        This method checks for a win in multiple directions
        
        Parameters
        ----------
        column (int)
                The column number of the current move.
        row  (int)
                The row number of the current move.
                
        Returns
        -------
        bool: True for a win and False if no win is found
        """
        # list of tuples containing all possibilities of offsetting values from the current index in order to identify wins. 
        # first value in each tuple represents the offset of the row and the second for the column
        # For example, the first tuple checks for a horizontal win since row has no offset while column is increasing. The last two
        # tuples check for diagnol wins; the third checks to the right while the fourth cheks to the left.
        # Althoug these offsetting directions only move in one direction, for example, the first tuple checks for a horizontal win
        # only from left to right and the same issue exists for  the rest of the tuples, but since the check_line function subtracts three
        # based on the values in the tuple we will always take into account all directions.  
        directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]
        
        # create a list of values returned from calling the check_line function using each tuple as a value for row and column offset.
        # the row and column parameters are obtained from what was passed to the function
        results = [self.check_line(row, col, dr, dc) for dr, dc in directions]
        
        # the list will be all false for no wins but will have one True if there is a win. The any function returns True if even
        # one of its values are true. So if there is a win the function reuturns True.
        return any(results)

    def check_line(self, row, col, dr, dc):
        """
        This method checks for four consecutive identical values based on the directions provided by dr and dc.
        
        Parameters
        ----------
        column (int)
                The column number of the current move.
        row  (int)
                The row number of the current move.
        dr  (int)
                The direction the function should move vertically.
        dc  (int)
                The direction the function should move horizontally.
        Returns
        -------
        bool: True if a consecutive line of four similar values are found and False if not.
        """
        #  initialize  a counter to hold the amount of consecutive values
        count = 0
        # for each direction provided by the 'dr' and 'dc' we offset the index by three so we can address the issue of only going in one direction
        # so if we are checking for consecutive horizontal values in a rightward direction we must move three steps backwards to account for the 
        # possibility that the consecutive values are to the left. This allows the loop to check all possible four consecutive values from the current
        # index while iterating seven times.
        row = row - dr * 3
        col = col - dc * 3
        # iterate seven times corresponding the width of the gameboard
        for _ in range(7):
        # since row and col can sometimes be negative, for example, when the index of row or column are less than three, so funciton tests for the out 
        # of range indexes. The second half of the condition is the actual test, which is if the original or new index that is now one step closer also
        #  has the same value as the step before it
            if 0 <= row < 6 and 0 <= col < 7 and self.board[row][col] == self.current_player:
        #  for each same value add one to the counter 
                count += 1
        # when four same values are recorded
                if count == 4:
        # functions returns true and loop stops even before seven iterations
                    return True
        # if any of the iterations yeild an index out of range or an opponents value, the count reverts back to zero
            else:
                count = 0
        # each iteration adds one (or zero which does nothing) to the index to explore the complete possible winning direction.
            row += dr
            col += dc
        # if after seven iterations four consecutive same values have not been found
        return False
