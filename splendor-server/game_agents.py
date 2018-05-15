from game_actions import *
import copy

class Agent:
    def __init__(self):
        self.state = None
        self.nodes_expanded = 0
        
    def next_action(self, game):
        actions = game.get_agent_actions()

        best_action = None
        max_utility = 0
        for action in actions:
            temp_board = copy.deepcopy(game.board)
            player = temp_board.get_current_player()
            temp_board.execute_action(player, action)
            temp_board.update_noble(player)

            utility = self.evaluate(temp_board.get_current_state(),
                                    temp_board.get_current_player())

            if utility > max_utility:
                best_action = action
                max_utility = utility

            del temp_board

        return best_action

    def prune_actions(self, actions):
        remaining_actions = []
        for action in actions:
            if type(action) != ReserveFromDeck:
                remaining_actions.append(action)
        return remaining_actions

    def next_action_maximax(self, game):
        self.nodes_expanded = 0
        current_player = game.board.get_current_player()
        actions = game.board.available_actions(current_player)
        best_action = None
        max_utility = 0
        for action in self.prune_actions(actions):
            self.level = 0
            temp_board = copy.deepcopy(game.board)

            nextAction = action
            while self.level < 5:
                nextPlayer = temp_board.get_current_player()
                temp_board.execute_action(nextPlayer, nextAction)
                temp_board.update_noble(nextPlayer)

                if temp_board.available_actions(nextPlayer) == []:
                    self.level += 1
                    if self.level == 5:
                        break
                    temp_board.next_player()

                nextAction = self.search_action(temp_board)

            utility = self.evaluate(temp_board.get_current_state(),
                                    temp_board.get_current_player())

            if utility > max_utility:
                max_utility = utility
                best_action = action

            del temp_board

        print('{} expanded {} nodes'.format(current_player.name, self.nodes_expanded))
        return best_action

    def search_action(self, board):
        actions = board.available_actions(board.get_current_player())

        best_action = None
        max_utility = 0
        for action in self.prune_actions(actions):
            temp_board = copy.deepcopy(board)
            player = temp_board.get_current_player()
            temp_board.execute_action(player, action)
            temp_board.update_noble(player)

            utility = self.evaluate(temp_board.get_current_state(),
                                    player)

            if utility > max_utility:
                best_action = action
                max_utility = utility

            del temp_board

        return best_action

    def evaluate(self, state, player):
        self.nodes_expanded += 1
        # score state
        score = 0
        score += (player.points * 3)
        score += min(player.total_coins_count(), 10)
        score += player.gold * 1.5

        score += (6* sum(player.gems) ** 0.8)

        # Deduct points for reservations
        score -= len(player.board_reservations)
        score -= len(player.deck_reservations)

        # print(player.name, score)
        # print("Coins", player.total_coins_count())
        return score
