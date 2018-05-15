from flask import Flask
from flask import request
from flask import jsonify
import json

from game_engine import *

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

game = None
agents = []

# @app.route('/start', methods=['POST'])
# def start():
#     # Starts game, returns state and actions for first player
#     print("Start")
#     names = json.loads(request.form['json'])
#     global game
#     game = MultiPlayerGame(names['player1'], names['player2'],
#                 names['player3'], names['player4'])
#     print(game.get_state())
#
#     return jsonify(game.get_state(), game.get_actions())
#
# @app.route('/game/<int:action_id>')
# def execute_action(action_id):
#     print("action id", action_id)
#     global game
#     if not game.has_ended():
#         game.execute_action(action_id)
#         if game.get_actions() == '[]':
#             # switches to next player if no action remaining
#             game.board.next_player()
#         return jsonify(game.get_state(), game.get_actions())
#     return 'Game Ended'

@app.route('/start', methods=['POST'])
def startSingle():
    global game
    global agents
    print("Start")
    names = json.loads(request.form['json'])
    game = SinglePlayerGame(names['player1'])
    #print(game.get_state())

    agents.append(Agent())
    #print(game.get_actions())
    return jsonify(game.get_state(), game.get_actions())

@app.route('/game/<int:action_id>')
def execute_action_single(action_id):
    print("action id", action_id)
    global game
    global agents
    if not game.has_ended():
        game.execute_action(action_id)
        if game.get_actions() == '[]':
            # switches to next player if no action remaining
            game.board.next_player()

            # agent moves
            while game.board.current_player != 0:
                game.execute_agent_action(agents[0].next_action(game))
                if game.get_actions() == '[]':
                    # switches to next player if no action remaining
                    game.board.next_player()

        return jsonify(game.get_state(), game.get_actions())
    print("Game Ended")
    return 'Game Ended'
