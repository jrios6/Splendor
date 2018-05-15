import numpy as np
import random
import itertools
from game_actions import *
from load_data import *
from helper import *
import jsonpickle
import json

class Noble:
    def __init__(self, points, red, blue, green, black, white, name):
        self.points = points
        self.red = red
        self.blue = blue
        self.green = green
        self.black = black
        self.white = white
        self.name = name

    def is_acquirable(self, red, blue, green, black, white):
        if red >= self.red and blue >= self.blue and green >= self.green and black >= self.black and white >= self.white:
            return True
        return False

    def __json__(self):
        return {'type': 'noble', 'points': self.points, 'red': self.red,
                'blue': self.blue, 'green': self.green, 'black': self.black,
                'white': self.white}

class NoblesDeck:
    def __init__(self):
        self.nobles = load_nobles_deck('data/nobles.csv')
        random.shuffle(self.nobles)

    def draw(self, count):
        return self.nobles[:count]


class Development:
    def __init__(self, points, tier, gem_type, red, blue, green, black, white):
        self.points = points
        self.tier = tier
        self.gem_type = gem_type
        self.red = red
        self.blue = blue
        self.green = green
        self.black = black
        self.white = white

    def is_buyable(self, red, blue, green, black, white, gold):
        gold_required = 0
        if self.red > red:
            gold_required += self.red - red
        if self.blue > blue:
            gold_required += self.blue - blue
        if self.green > green:
            gold_required += self.green - green
        if self.black > black:
            gold_required += self.black - black
        if self.white > white:
            gold_required += self.white - white
        if gold >= gold_required:
            return True
        return False

    def describe(self):
        print("This is a tier {} {} card. {} red, {} blue, {} green, {} black, \
            {} white required. Gives {} points.".format(self.tier, self.gem_type,
            self.red, self.blue, self.green, self.black, self.white, self.points))

    def description_text(self):
        text = "Tier {} {} card. {} red, {} blue, {} green, {} black, \
            {} white required. Gives {} points.".format(self.tier, self.gem_type,
            self.red, self.blue, self.green, self.black, self.white, self.points)
        return text

    def __json__(self):
        return {'type': 'development', 'points': self.points, 'tier': self.tier,
                'gem_type': self.gem_type, 'red': self.red, 'blue': self.blue,
                'green': self.green, 'black': self.black, 'white': self.white}


class Deck:
    def __init__(self, tier):
        self.tier = tier
        # init deck with cards
        path = 'data/tier{}.csv'.format(tier)
        self.cards = load_development_deck(path)
        # shuffle deck
        random.shuffle(self.cards)

    def draw(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        return False

    def isEmpty(self):
        return len(self.cards) == 0


class Player:
    def __init__(self, name, treasury):
        self.name = name
        self.points = 0
        self.developments = []
        self.board_reservations = []
        self.deck_reservations = []
        self.nobles = []
        self.gems = [0, 0, 0, 0, 0]
        self.gem_dict = {'red': 0, 'blue': 1, 'green': 2, 'white': 3, 'black': 4}
        self.treasury = treasury
        self.red = 0
        self.blue = 0
        self.green = 0
        self.black = 0
        self.white = 0
        self.gold = 0

    def __json__(self):
        return {'type': 'player', 'name': self.name, 'points': self.points, 'gems': self.gems,
                'developments': self.developments, 'board_reservations': self.board_reservations,
                'deck_reservations': self.deck_reservations, 'nobles': self.nobles,
                'red': self.red, 'blue': self.blue, 'green': self.green, 'black': self.black,
                'white': self.white, 'gold': self.gold}

    def purchasable_cards(self, cards):
        """Returns array of purchasable cards in cards array"""
        purchasable_cards = []
        for card in cards:
            if card and card.is_buyable(self.red + self.gem_count("red"),
                                self.blue + self.gem_count("blue"),
                                self.green + self.gem_count("green"),
                                self.black + self.gem_count("black"),
                                self.white + self.gem_count("white"),
                                self.gold):
                purchasable_cards.append(card)
        return purchasable_cards

    def add_gem(self, color):
        """Add gem of color"""
        idx = self.gem_dict[color]
        self.gems[idx] += 1

    def gem_count(self, color):
        idx = self.gem_dict[color]
        return self.gems[idx]

    def acquire_noble(self, noble):
        self.nobles.append(noble)
        self.points += noble.points

    def total_coins_count(self):
        return self.white + self.red + self.blue + self.black + self.green + self.gold

    def remove_coins_to_treasury(self, color, num):
        if color == 'red':
            self.red -= num
            self.treasury.add_coins("red", num)
        if color == 'blue':
            self.blue -= num
            self.treasury.add_coins("blue", num)
        if color == 'black':
            self.black -= num
            self.treasury.add_coins("black", num)
        if color == 'white':
            self.white -= num
            self.treasury.add_coins("white", num)
        if color == 'green':
            self.green -= num
            self.treasury.add_coins("green", num)
        if color == 'gold':
            self.gold -= num
            self.treasury.add_coins("gold", num)

    def purchase_card(self, card):
        """Assumes card is purchasable"""
        # net spending required for each color
        net_red = max(card.red - self.gem_count("red"), 0)
        net_blue = max(card.blue - self.gem_count("blue"), 0)
        net_black = max(card.black - self.gem_count("black"), 0)
        net_green = max(card.green - self.gem_count("green"), 0)
        net_white = max(card.white - self.gem_count("white"), 0)

        # deduct net spending from coins, use gold coins if insufficient
        if self.red >= net_red:
            self.remove_coins_to_treasury("red", net_red)
        else:
            self.remove_coins_to_treasury("gold", net_red - self.red)
            self.remove_coins_to_treasury("red", self.red)

        if self.blue >= net_blue:
            self.remove_coins_to_treasury("blue", net_blue)
        else:
            self.remove_coins_to_treasury("gold", net_blue - self.blue)
            self.remove_coins_to_treasury("blue", self.blue)

        if self.green >= net_green:
            self.remove_coins_to_treasury("green", net_green)
        else:
            self.remove_coins_to_treasury("gold", net_green - self.green)
            self.remove_coins_to_treasury("green", self.green)

        if self.black >= net_black:
            self.remove_coins_to_treasury("black", net_black)
        else:
            self.remove_coins_to_treasury("gold", net_black - self.black)
            self.remove_coins_to_treasury("black", self.black)

        if self.white >= net_white:
            self.remove_coins_to_treasury("white", net_white)
        else:
            self.remove_coins_to_treasury("gold", net_white - self.white)
            self.remove_coins_to_treasury("white", self.white)


        # add gem to user
        self.add_gem(card.gem_type)

        # add card to player
        self.developments.append(card)

        # update player points count
        self.points += card.points

class Treasury:
    def __init__(self):
        self.coins = [7, 7, 7, 7, 7, 5]
        self.name_dict = {'red': 0, 'blue': 1, 'green': 2, 'black': 3, 'white': 4, 'gold': 5}

    def add_coins(self, color, num):
        """Add num coins of color"""
        idx = self.name_dict[color]
        self.coins[idx] += num

    def remove_coins(self, color, num):
        """Remove num coins of color, returns True if successful, False otherwise"""
        idx = self.name_dict[color]
        if self.coins[idx] >= num:
            self.coins[idx] -= num
            return True
        return False

    def remaining_colored_coins(self):
        return sum(self.coins[:5])

    def get_actions(self):
        actions = []
        # indexes with coin > 0
        valid_indexes = [i for i in range(5) if self.coins[i] > 0]
        comb_length = len(valid_indexes)
        if len(valid_indexes) >= 3:
            comb_length = 3
        elif len(valid_indexes) == 0:
            return []

        # generate tuples of combination (1 coin per color)
        combinations = list(itertools.combinations(valid_indexes, comb_length))
        for comb in combinations:
            # convert tuple to coin
            coin_required = [0, 0, 0, 0, 0, 0]
            for idx in comb:
                coin_required[idx] += 1

            actions.append(CollectCoins(coin_required[0], coin_required[1], coin_required[2],
                                        coin_required[3], coin_required[4], coin_required[5]))


        # indexes with coin >= 4
        valid_indexes = [i for i in range(5) if self.coins[i] >= 4]

        # generate tuples of combination (2 coin per color)
        combinations = list(itertools.combinations(valid_indexes, 1))
        for comb in combinations:
            # convert tuple to coin
            coin_required = [0, 0, 0, 0, 0, 0]
            red = blue = green = black = white = gold = 0
            for idx in comb:
                coin_required[idx] += 2

            actions.append(CollectCoins(coin_required[0], coin_required[1], coin_required[2],
                                        coin_required[3], coin_required[4], coin_required[5]))


        return actions

    def describe(self):
        print("There are {} red, {} blue, {} green, {} black, {} white, {} gold coins in \
            the treasury".format(self.coins[0], self.coins[1], self.coins[2],
            self.coins[3], self.coins[4], self.coins[5]))

    def __json__(self):
        return {'type': 'treasury', 'red': self.coins[0], 'blue': self.coins[1],
                'green': self.coins[2], 'black': self.coins[3], 'white': self.coins[4],
                'gold': self.coins[5]}


class Board:
    def __init__(self, player1, player2, player3, player4):
        self.treasury = Treasury()
        self.players = [Player(player1, self.treasury), Player(player2, self.treasury),
                        Player(player3, self.treasury), Player(player4, self.treasury)]

        self.deck_tier_1 = Deck(1)
        self.deck_tier_2 = Deck(2)
        self.deck_tier_3 = Deck(3)

        self.nobles = []

        self.leaderboard = [0, 0, 0, 0]

        self.open_tier_1 = []
        self.open_tier_2 = []
        self.open_tier_3 = []

        self.round = 0
        self.current_player = 0
        self.should_discard_coin = False

    def __json__(self):
        return {'type': 'board', 'leaderboard': self.leaderboard, 'round': self.round,
                'current_player': self.current_player, 'should_discard_coin': self.should_discard_coin,
                'players': self.players, 'treasury': self.treasury, 'open_tier_1': self.open_tier_1,
                'open_tier_2': self.open_tier_2, 'open_tier_3': self.open_tier_3, 'nobles': self.nobles}

    def start_game(self):
        """Draws nobles from Nobles Deck and cards from Cards Deck"""
        self.nobles = NoblesDeck().draw(5)
        for i in range(4):
            self.open_tier_1.append(self.deck_tier_1.draw())
            self.open_tier_2.append(self.deck_tier_2.draw())
            self.open_tier_3.append(self.deck_tier_3.draw())

    def get_current_player(self):
        """Returns the current player"""
        return self.players[self.current_player]


    def next_player(self):
        """Increments player count or reset to 0 if round is completed"""
        self.current_player += 1
        self.should_discard_coin = False
        if self.current_player >= len(self.players):
            self.round += 1
            self.current_player = 0

    def get_current_state(self):
        """Prints current state of board"""
        # development cards
        # for card in self.open_tier_1 + self.open_tier_2 + self.open_tier_3:
        #     if card:
        #         card.describe()

        # treasury
        #self.treasury.describe()
        return json.dumps(self, cls=MyEncoder)


    def available_actions(self, player):
        """Return available legal actions for player"""
        legal_actions = []

        if self.should_discard_coin:
            return self.get_coin_discard_actions(player)

        # buy development card
        purchasable_cards = []
        purchasable_cards += player.purchasable_cards(self.open_tier_1)
        purchasable_cards += player.purchasable_cards(self.open_tier_2)
        purchasable_cards += player.purchasable_cards(self.open_tier_3)
        purchasable_cards += player.purchasable_cards(player.board_reservations)
        purchasable_cards += player.purchasable_cards(player.deck_reservations)

        for card in purchasable_cards:
            legal_actions.append(PurchaseDevelopment(card))

        if len(player.board_reservations) + len(player.deck_reservations) < 3:
            # reserve open development cards
            for card in self.open_tier_1 + self.open_tier_2 + self.open_tier_3:
                if card:
                    legal_actions.append(ReserveOpenDevelopment(card))

            # reserve from top of deck
            if not self.deck_tier_1.isEmpty():
                legal_actions.append(ReserveFromDeck(0))

            if not self.deck_tier_2.isEmpty():
                legal_actions.append(ReserveFromDeck(1))

            if not self.deck_tier_3.isEmpty():
                legal_actions.append(ReserveFromDeck(2))

        # collect coins
        legal_actions += self.treasury.get_actions()

        # assigning option id to each action
        for i in range(len(legal_actions)):
            legal_actions[i].option = i

        return legal_actions


    def execute_action(self, player, action):
        if type(action) == ReserveOpenDevelopment:
            # add card to player's reservation
            player.board_reservations.append(action.card)

            # remove card from open tier and draw new card from deck
            if action.card in self.open_tier_1:
                self.open_tier_1.remove(action.card)
                self.open_tier_1.append(self.deck_tier_1.draw())
            elif action.card in self.open_tier_2:
                self.open_tier_2.remove(action.card)
                self.open_tier_2.append(self.deck_tier_2.draw())
            elif action.card in self.open_tier_3:
                self.open_tier_3.remove(action.card)
                self.open_tier_3.append(self.deck_tier_3.draw())

            # add 1 gold coin to player if available and remove from treasury
            if self.treasury.remove_coins("gold", 1):
                player.gold += 1


        elif type(action) == ReserveFromDeck:
            # draw top card from deck to player's reservation
            decks = [self.deck_tier_1, self.deck_tier_2, self.deck_tier_3]
            player.deck_reservations.append(decks[action.deck].draw())

            # add 1 gold coin to player if available and remove from treasury
            if self.treasury.remove_coins("gold", 1):
                player.gold += 1


        elif type(action) == CollectCoins:
            # add coins to player, remove coins from treasury
            player.red += action.red
            self.treasury.remove_coins("red", action.red)

            player.blue += action.blue
            self.treasury.remove_coins("blue", action.blue)

            player.green += action.green
            self.treasury.remove_coins("green", action.green)

            player.white += action.white
            self.treasury.remove_coins("white", action.white)

            player.black += action.black
            self.treasury.remove_coins("black", action.black)

            player.gold += action.gold
            self.treasury.remove_coins("gold", action.gold)


        elif type(action) == PurchaseDevelopment:
            # add card to player
            player.purchase_card(action.card)

            # remove card from open tier/ player reservations and draw new card
            if action.card in self.open_tier_1:
                self.open_tier_1.remove(action.card)
                self.open_tier_1.append(self.deck_tier_1.draw())
            elif action.card in self.open_tier_2:
                self.open_tier_2.remove(action.card)
                self.open_tier_2.append(self.deck_tier_2.draw())
            elif action.card in self.open_tier_3:
                self.open_tier_3.remove(action.card)
                self.open_tier_3.append(self.deck_tier_3.draw())
            elif action.card in player.board_reservations:
                player.board_reservations.remove(action.card)
            elif action.card in player.deck_reservations:
                player.deck_reservations.remove(action.card)

            # update leaderboard
            self.update_leaderboard(player)


        elif type(action) == DiscardCoins:
            player.remove_coins_to_treasury("red", action.red)
            player.remove_coins_to_treasury("blue", action.blue)
            player.remove_coins_to_treasury("green", action.green)
            player.remove_coins_to_treasury("black", action.black)
            player.remove_coins_to_treasury("white", action.white)
            player.remove_coins_to_treasury("gold", action.gold)

        if not self.should_discard_coin:
            # set discard coin routine after executing action
            self.should_discard_coin = True


    def update_leaderboard(self, player):
        idx = self.players.index(player)
        self.leaderboard[idx] = player.points


    def update_noble(self, player):
        # check if player has enough gems to get a noble
        for noble in self.nobles:
            if noble.is_acquirable(player.gem_count("red"), player.gem_count("blue"),
                                   player.gem_count("green"), player.gem_count("black"),
                                   player.gem_count("white")):
                # add noble to player and
                # remove noble from nobles deck
                player.acquire_noble(noble)
                self.nobles.remove(noble)

                # update leaderboard
                self.update_leaderboard(player)


    def get_coin_discard_actions(self, player):
        """Generate discard coins action for each possible coin combination"""
        actions = []
        if player.total_coins_count() > 10:
            # max to 3
            coins_to_discard = player.total_coins_count() - 10
            coins = [player.red, player.blue, player.green,
                     player.black, player.white, player.gold]

            if coins_to_discard == 1:
                for i in range(6):
                    if coins[i] > 0:
                        discard = [0] * i + [1] + [0] * (5-i)
                        actions.append(DiscardCoins(discard[0], discard[1],
                                        discard[2], discard[3], discard[4],
                                        discard[5]))

            elif coins_to_discard == 2:
                index_more_than_1 = [i for i in range(6) if coins[i] > 1]
                index_more_than_0 = [i for i in range(6) if coins[i] > 0]
                # combinations of 2 coin
                for i in index_more_than_1:
                    discard = [0] * 6
                    discard[i] = 2
                    actions.append(DiscardCoins(discard[0], discard[1],
                                    discard[2], discard[3], discard[4],
                                    discard[5]))

                # combinations of 1 coin
                for i in range(len(index_more_than_0)):
                    for j in range(i+1, len(index_more_than_0)):
                        if index_more_than_0[i] != index_more_than_0[j]:
                            discard = [0] * 6
                            discard[index_more_than_0[i]] = discard[index_more_than_0[j]] = 1
                            actions.append(DiscardCoins(discard[0], discard[1],
                                            discard[2], discard[3], discard[4],
                                            discard[5]))

            elif coins_to_discard == 3:
                index_more_than_2 = [i for i in range(6) if coins[i] > 2]
                index_more_than_1 = [i for i in range(6) if coins[i] > 1]
                index_more_than_0 = [i for i in range(6) if coins[i] > 0]
                # combinations of 2, 1 coin
                for i in index_more_than_1:
                    for j in index_more_than_0:
                        if i != j:
                            discard = [0] * 6
                            discard[i] = 2
                            discard[j] = 1
                            actions.append(DiscardCoins(discard[0], discard[1],
                                            discard[2], discard[3], discard[4],
                                            discard[5]))
                # combinations of 3 coin
                for i in index_more_than_2:
                    discard = [0] * 6
                    discard[i] = 3
                    actions.append(DiscardCoins(discard[0], discard[1],
                                    discard[2], discard[3], discard[4],
                                    discard[5]))

                # combinations of 1 coin
                for i in range(len(index_more_than_0)):
                    for j in range(i+1, len(index_more_than_0)):
                        for k in range(j+1, len(index_more_than_0)):
                            if index_more_than_0[i] != index_more_than_0[j] and index_more_than_0[j] != index_more_than_0[k]:
                                discard = [0] * 6
                                discard[index_more_than_0[i]] = discard[index_more_than_0[j]] = discard[index_more_than_0[k]] = 1
                                actions.append(DiscardCoins(discard[0], discard[1],
                                                discard[2], discard[3], discard[4],
                                                discard[5]))
        # assigning option id to each action
        for i in range(len(actions)):
            actions[i].option = i

        return actions


    def game_has_ended(self):
        """True if a player has at least 15 points"""
        return max(self.leaderboard) >= 15
