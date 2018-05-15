# Splendor  
This project is a replication of the popular Splendor boardgame, designed for AI development. Splendor is a easy-to-learn, yet complex zero-sum boardgame that requires strategic thinking, deception, adverserial tactics, player cooperation and logical computation.

While you can play against AI today through the existing Splendor iOS and Andrioid app, the agents are relatively weak and are below human-level performance. The primary goal of this project is to develop game-playing Agents using classical and deep reinforcement learning techniques that can surpass existing AI and top players in the game.


## The game
"Splendor is a game of chip-collecting and card development. Players are merchants of the Renaissance trying to buy gem mines, means of transportation, shops—all in order to acquire the most prestige points. If you're wealthy enough, you might even receive a visit from a noble at some point, which of course will further increase your prestige." -- [BoardGameGeek](https://boardgamegeek.com/boardgame/148228/splendor)

## Usage

The project consists of a React Client and a Flask Server. You will require Node >= 6, Python 3 and Flask installed on your local development machine.

### Running the client
```
$ cd splendor-client
$ npm start
```

### Running the server

```
$ cd splendor-server
$ FLASK_APP=app.py flask run
```

With that, you can start playing against the AI on using at http://localhost:3000/.

## What's next?
This project is currently under development and there are alot of fixes, code refactoring and features to look forward to!
- Improvements to Client UI (e.g. preventing users from double clicking, nicer card background, background music, highlighting last move made, better coin selection action)
- Using pruning techniques to improve efficiency of game tree exploration
- Deeper exploration to allow more strategic foward thinking reservation/ gem collection moves.
- Framework for evaluating and improving heuristic function
- Fixes: Random ordering of AI/Human players and preventing AI from looking at next card
