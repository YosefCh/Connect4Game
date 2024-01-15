import Connect4Game
import Random_move as rand
import AI_player as ap
import copy
import func_timeout

competitor_list = [ap.AI_strategy(), rand.RandomStrategy("alter ego")]

MAX_WAIT_TIME = 1
winners = list()
random_choice = rand.RandomStrategy()

for game_nr in range(100):
    print(game_nr + 1)
    tie = False
    game = Connect4Game.Connect4Game()
    while game.winner is None:
        game_safety_copy = copy.deepcopy(game)
        try:
            move = func_timeout.func_timeout(
                MAX_WAIT_TIME, competitor_list[game.current_player - 1].strategy, [game_safety_copy])
        except func_timeout.FunctionTimedOut:
            print(f'time out limit exceeded: {competitor_list[game.current_player - 1].name} performs random move')
            move = random_choice.strategy(game_safety_copy)
        game.make_move(move)
        if 0 == sum(map(game.is_valid_move, range(7))):
            tie = True
            break
    if tie:
        winners.append("tie")
    else:
        winners.append(competitor_list[game.current_player - 1].name)
    competitor_list.reverse()

dictionary = {}
for item in winners:
    dictionary[item] = dictionary.get(item, 0) + 1

print(dictionary)