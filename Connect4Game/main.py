# import Connect4Game file for its class
import Connect4Game
# same for this file and its classes
import Random_move as rand
# import the copy module to use deepcopy to make a safe copy of the instance we are using
import copy
# import func_timeout module to set a time limit on each move
import func_timeout

# list of instances of the RandomStrategy class. One uses default name while the other is provided
competitor_list = [rand.RandomStrategy(), rand.RandomStrategy("alter ego")]

# wait time of one second for a move using the strategy method further in the code.
MAX_WAIT_TIME = 1
# initialize a list to record number of wins per player and the number of ties
winners = list()
# instance of of the RandomStrategy class that has all the functionality of the Connect4Game class but with the addition
# of the strategy method that can generate random valid moves
random_choice = rand.RandomStrategy()

# iterate through 1,000 games
for game_nr in range(1000):
    
# print the number of each game while computation is taking place so user wont't think program isn't working
# during the 15 seconds or so that it takes the run the program
    print(game_nr + 1)
    
# set tie to false since if there was a tie in the previous game, tie was set to true
    tie = False
# create an instance of the Connect4Game class to have access the make move and is_valid_move functions
    game = Connect4Game.Connect4Game()

# as long as there is no winner which is determined by the make_move function calling the check_winner and check_line fuctions.
# this loop is for each of the 1,000 games and will break after all the moves have been made or if there is a winner
    while game.winner is None:
        
# make a safe copy of the game instance of the Connect4GAme class. This type of copy is completely separate from the original
# game instance and changes made to one will not affect the other. I don't understand the need for a deepcopy in this scenario
# since the strategy method isn't modifying the game state at all but is just generating a random valid move. I am assumin that 
# this is just protocol for programming games
        game_safety_copy = copy.deepcopy(game)
        
# the try and except clause implies that the code in the except clause will not produce the same potential
# errors that the try code might. However, the code given to both are identical; they are both using the
# strategy method which has the game_safety_copy passed to it. Perhaps the reason to use the try and except
# is if the computation gets stuck we can sort of do a restart (I don't know if this understanding is correct
# at all). I actually made a copy of this file and removed the func_timeout with the try and except and ran
# the code and had the exact same performance as before. I realized afterwards that I didn't have to run the 
# code without the func_timeout and try except to to see that there is no need for the try and except. 
# The mere fact that the code ran 1,000 games in  about 13 seconds is proof that no timeout was ever being reached
# since each complete game only took 13/1000 seconds! so each move was at most seven times less than that (since it
# takes a minimum of seven moves to complete a game). And in reality a game played with random moves probably has
# far more than seven moves in a game.
        try:
            
# variable to be fed to the make_move function. It uses the func_timeout to set max time of one second to choose a 
# move. The unusual syntax of brackets instead of parentheses (as it is in the except clause) is due to the specifics
# of the func_timeout function.
# the competitor is referenced by using the values of the players identifying numbers which are 1 and 2. When subtracting
# 1 from either of these numbers one gets either 0 or 1 which are the indexes of the values contained in the competitor
# list. This allows alternating between turns of the competitors.
            move = func_timeout.func_timeout(
                MAX_WAIT_TIME, competitor_list[game.current_player - 1].strategy, [game_safety_copy])
        except func_timeout.FunctionTimedOut:
# print error message using f strings refferencing the current player's name indicating that a random move is being made
            print(f'time out limit exceeded: {competitor_list[game.current_player - 1].name} performs random move')
            
# use the random_choice instance of the of RandomStrategy with the strategy method. See above that I don't really understand
# the point of this
            move = random_choice.strategy(game_safety_copy)
# make the move produced by strategy. 
        game.make_move(move)
# after each move, check if game is over by iterating over all columns from 0-6 and testing if any are valid moves.
# this is done by mapping the is_valid_move function on all these possibilites and creating a list of booleans. 
# The list is then summed to see if there are any True values which means that there are still valid moves left on
# the board since true has a value of 1 and false a value of zero. The while loop will continue until the sum of the
# of the mapped is_valid_move is zero meaning no moves are left or is there is a winner which would be determined by 
# make_move function earlier. In addition, If the sum is zero that means that there must be a tie since no win has been detected
        if 0 == sum(map(game.is_valid_move, range(7))):
            
# set tie to true to be used as a test to see if a tie should be added to the winners list
            tie = True
# break out of while loop for this game
            break
    if tie:
# add a tie to the winners list which holds the game results
        winners.append("tie")
    else:
# the current player who stopped the while loop after his move must be the winner so get his name from the competitor list and 
# add it to the winners list
        winners.append(competitor_list[game.current_player - 1].name)
# list is reversed therby alternating the first turn of the game between players
    competitor_list.reverse()

# create dictionary to display the results of all 1,000 games
dictionary = {}
# loop through all results stored in the winners list
for item in winners:
    
# For each unique item in the winners list a new key will be created since dictionaries can only have unique keys so there will 
# only be keys for player names and for tie. The code further tries to access the value of the key and add one to  it for each time
# it appears in the winners list. However, the first time a potential key is encountered in the list it is not yet a key and therfore 
# has no value and returns the second arg given which is a zero. To bypass this problem, 1 is added to the zero value to count for the 
# occurence of the key in the list. In subsequent occurences of the item in the list 1 is also added every time.
    dictionary[item] = dictionary.get(item, 0) + 1
    
# display the dictionary with all the results
print(dictionary)
