from game_actions import *
import copy

class Agent:
    def __init__(self):
        self.state = None
        self.nodes_expanded = 0

    def next_action(self, game):
        """
        Evaluates next state and return action with highest utility
        """
        self.current_player = game.board.get_current_player()
        return self.search_action(game.board)

    def prune_actions(self, actions):
        remaining_actions = []
        for action in actions:
            # remove reservation from deck action
            if type(action) != ReserveFromDeck:
                remaining_actions.append(action)
        return remaining_actions

    def next_action_search(self, game):
        """
        Recursively expands node with highest utility to a depth of 5.
        """
        self.nodes_expanded = 0
        self.current_player = game.board.get_current_player()
        actions = game.board.available_actions(self.current_player)
        best_action = actions[0]
        max_utility = -99

        for action in self.prune_actions(actions):
            depth = 0
            temp_board = copy.deepcopy(game.board)
            nextAction = action
            action.describe()

            while depth < 5:
                nextPlayer = temp_board.get_current_player()
                temp_board.execute_action(nextPlayer, nextAction)
                temp_board.update_noble(nextPlayer)

                if temp_board.available_actions(nextPlayer) == []:
                    depth += 1
                    if depth == 5:
                        break
                    temp_board.next_player()

                nextAction = self.search_action(temp_board)

            utility = self.evaluate(temp_board,
                                    temp_board.get_current_player())

            if utility > max_utility:
                max_utility = utility
                best_action = action

            del temp_board
        print("Max Utility", max_utility)
        print('{} expanded {} nodes'.format(self.current_player.name, self.nodes_expanded))
        return best_action

    def search_action(self, board):
        actions = board.available_actions(board.get_current_player())

        best_action = actions[0]
        max_utility = -99
        for action in self.prune_actions(actions):
            temp_board = copy.deepcopy(board)
            player = temp_board.get_current_player()
            temp_board.execute_action(player, action)
            temp_board.update_noble(player)

            utility = self.evaluate(temp_board,
                                    player)

            if utility > max_utility:
                best_action = action
                max_utility = utility

            del temp_board

        return best_action

    def evaluate(self, board, player):
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

        if max(board.leaderboard) >= 15 and player.points < 15 and player.name == self.current_player.name:
            # negative points if terminal state is a loss
            print(-sum(i >= 15 for i in board.leaderboard), "for ", player.name)
            # -1 point for each player >= 15
            return -sum(i >= 15 for i in board.leaderboard)

        if player.points >= 15:
            score += 10000

        return score
