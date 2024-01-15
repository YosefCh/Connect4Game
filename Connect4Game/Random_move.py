import Connect4Game as Game
import random


class RandomStrategy(Game.Connect4GameStrategy):
    """
    This class inherits from the abstract class Connect4GameStrategy and provides implementaion of the strategy method.
    
    Instance Variables
    ------------------
    self.name: (str) 
              Optional parameter with default value
    
    Methods
    -------
    
    strategy: This method recieves the Connect4Game class or a copy of it and generates a random
               valid move.
    
    """
    def __init__(self, name="Daniel Batyrev"):
        self.name = name
    
    # the strategy method is a class method hence the cls refers to class (instead of the self which refers to the instance of the class).
    # since the strategy method dosn't need to modify any instance but just needs access to the class and its methods it is made a class method
    @classmethod
    def strategy(cls, game_safety_copy):
        """
        This method recieves a Connect4Game class or a copy of it and generates a random
        valid move.
        
        Parameters
        ----------
        game_safety_copy (int)
                The column number of the current move.
                
        Returns
        -------
        int: a number representing the column of the move to make
        """
        # initialize a list to hold all the valid moves
        valid_moves = list()
        # loop from 0-6 as those are the column indexes of the board
        for col in range(7):
        # if a specific col is a valid move approved by the is_valid_move function
            if game_safety_copy.is_valid_move(col):
        # append the move to the list
                valid_moves.append(col)
        # use random to choose a move from the list
        return random.choice(valid_moves)

