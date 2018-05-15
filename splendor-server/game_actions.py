class Action:
    def __init__(self):
        self.option = None

class ReserveOpenDevelopment(Action):
    def __init__(self, card):
        self.card = card

    def describe(self):
        print("Reserve open development: {}".format(self.card.description_text()))

    def __json__(self):
        return {'type': 'reserve_open_development', 'card': self.card, 'option': self.option}

class ReserveFromDeck(Action):
    def __init__(self, deck_num):
        self.deck = deck_num

    def describe(self):
        print("Reserve directly from tier {} deck".format(self.deck + 1))

    def __json__(self):
        return {'type': 'reserve_from_deck', 'deck_num': self.deck, 'option': self.option}

class PurchaseDevelopment(Action):
    def __init__(self, card):
        self.card = card

    def describe(self):
        print("Purchase development: {}".format(self.card.description_text()))

    def __json__(self):
        return {'type': 'purchase_development', 'card': self.card, 'option': self.option}

class CollectCoins(Action):
    def __init__(self, red, blue, green, black, white, gold):
        self.red = red
        self.blue = blue
        self.green = green
        self.black = black
        self.white = white
        self.gold = 0

    def describe(self):
        print("Collect coins from Treasury: {} red, {} blue, {} green, {} black, {} white.".format(self.red,
            self.blue, self.green, self.black, self.white))

    def __json__(self):
        return {'type': 'collect_coins', 'red': self.red, 'blue': self.blue, 'green': self.green,
                'black': self.black, 'white': self.white, 'gold': self.gold, 'option': self.option}

class DiscardCoins(Action):
    def __init__(self, red, blue, green, black, white, gold):
        self.red = red
        self.blue = blue
        self.green = green
        self.black = black
        self.white = white
        self.gold = gold

    def describe(self):
        print("Discarding coins: {} red, {} blue, {} green, {} black, {} white, {} gold".format(self.red,
            self.blue, self.green, self.black, self.white, self.gold))

    def __json__(self):
        return {'type': 'discard_coins', 'red': self.red, 'blue': self.blue, 'green': self.green,
                'black': self.black, 'white': self.white, 'gold': self.gold, 'option': self.option}
