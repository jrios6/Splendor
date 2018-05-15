from game_resources import *
from game_actions import *
from game_agents import *
from helper import *
import json
import copy

# APIS

# Start game (player name 1, 2, 3, 4)
# returns game state and sequence

# Action (collect coin, how many)
# Action (reserve from deck)
# Action (reserve from board)
# Action (purchase development)

# Action (discard coin)

class MultiPlayerGame:
    def __init__(self, player1, player2, player3, player4):
        # Init board with players
        self.board = Board(player1, player2, player3, player4)
        self.board.start_game()

    def has_ended(self):
        return self.board.game_has_ended()

    def get_state(self):
        return self.board.get_current_state()

    def get_actions(self):
        player = self.board.get_current_player()
        available_actions = self.board.available_actions(player)
        return json.dumps(available_actions, cls=MyEncoder)

    def execute_action(self, choice):
        player = self.board.get_current_player()
        available_actions = self.board.available_actions(player)
        action = available_actions[choice]

        # execute action
        self.board.execute_action(player, action)
        self.board.update_noble(player)

class SinglePlayerGame:
    def __init__(self, player1):
        # Init board with players
        # Assume human starts first
        self.board = Board(player1, 'player2', 'player3', 'player4')
        self.board.start_game()

    def has_ended(self):
        return self.board.game_has_ended()

    def get_state(self):
        return self.board.get_current_state()

    def get_actions(self):
        player = self.board.get_current_player()
        available_actions = self.board.available_actions(player)

        return json.dumps(available_actions, cls=MyEncoder)

    def get_agent_actions(self):
        player = self.board.get_current_player()
        return self.board.available_actions(player)

    def execute_action(self, choice):
        player = self.board.get_current_player()
        available_actions = self.board.available_actions(player)
        action = available_actions[choice]

        # execute action
        self.board.execute_action(player, action)
        self.board.update_noble(player)

    def execute_agent_action(self, action):
        player = self.board.get_current_player()
        self.board.execute_action(player, action)
        self.board.update_noble(player)



def game_engine():
    # Get name of players
    player_names = []
    for i in range(4):
        player_names.append(input())

    # Init board with players
    board = Board(player_names[0], player_names[1], player_names[2], player_names[3])
    board.start_game()

    # while game not end (points = 15)
    while not board.game_has_ended():
        # for each round
        for turn in range(4):
            # get next player
            player = board.get_current_player()

            # print current state
            board.get_current_state()

            # return action options
            available_actions = board.available_actions(player)
            for idx in range(len(available_actions)):
                print("Option {}".format(idx))
                available_actions[idx].describe()

            print("Player", player.name)


            # wait for player option
            choice = input()
            while not choice.isdigit() or int(choice) < 0 or int(choice) >= len(available_actions):
                choice = input()

            action = available_actions[int(choice)]
            # execute action
            board.execute_action(player, action)


            # Coin Discard
            available_actions = board.available_actions(player)
            if available_actions != []:
                for idx in range(len(available_actions)):
                    print("Option {}".format(idx))
                    available_actions[idx].describe()

                # wait for player option
                choice = input()
                while not choice.isdigit() or int(choice) < 0 or int(choice) >= len(available_actions):
                    choice = input()

                action = available_actions[int(choice)]
                board.execute_action(player, action)
                board.update_noble(player)

            # update game state
            board.next_player()


if __name__ == "__main__":
    game_engine()
