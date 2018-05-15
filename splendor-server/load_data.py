import numpy as np
import game_resources

def load_development_deck(path):
    deck_data = np.loadtxt(open(path, "rb"), dtype='S10', delimiter=",", skiprows=1)

    deck = []
    for row in deck_data:
        tier = int(row[0])
        white = int(row[1])
        blue = int(row[2])
        green = int(row[3])
        red = int(row[4])
        black = int(row[5])
        gem_type = row[6].decode('UTF-8')
        points = int(row[7])

        deck.append(game_resources.Development(points, tier, gem_type, red, blue, green, black, white))

    return deck


def load_nobles_deck(path):
    deck_data = np.loadtxt(open(path, "rb"), dtype='int', delimiter=",", skiprows=1)

    deck = []
    for row in deck_data:
        points = int(row[0])
        white = int(row[1])
        blue = int(row[2])
        green = int(row[3])
        red = int(row[4])
        black = int(row[5])

        deck.append(game_resources.Noble(points, red, blue, green, black, white, 'Jerry'))

    return deck
