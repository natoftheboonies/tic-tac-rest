import random, string

from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)

api = Api(app)

GAMES = {}

def abort_if_game_doesnt_exist(game_id):
    if game_id not in GAMES:
        abort(404, message="Game {} doesn't exist".format(game_id))

parser = reqparse.RequestParser()
parser.add_argument('X')
parser.add_argument('O')
parser.add_argument('player')

VALID = [0,1,2,10,11,12,20,21,22]

WINS = [
    set([0,1,2]),
    set([10,11,12]),
    set([20,21,22]),
    set([0,10,20]),
    set([1,11,21]),
    set([2,12,22]),
    set([0,11,22]),
    set([2,11,20])
]

assert(all([len(win) == 3 for win in WINS]))

class Game(Resource):

    def get(self, game_id):
        abort_if_game_doesnt_exist(game_id)
        return GAMES[game_id]

    def put(self, game_id):
        abort_if_game_doesnt_exist(game_id)
        args = parser.parse_args()
        game = GAMES[game_id]
        if game["turn"] == "X" and args['X']:
            play = int(args['X'])
            if play in game["O"] or play in game['X'] or play not in VALID:
                abort(401, message="play {} is invalid for game {}".format(play, game_id))
            else:
                game["X"].append(play)
                game["turn"] = "O"
        elif game["turn"] == "O" and args['O']:
            play = int(args['O'])
            if play in game["O"] or play in game['X'] or play not in VALID:
                abort(401, message="play {} is invalid for game {}".format(play, game_id))
            else:
                game["O"].append(play)
                game["turn"] = "X"
        else:
            print("invalid request", game_id, args)    
            abort(401, message="invalid request for game {}".format(game_id))

        # check for win
        if any([win.issubset(game['X']) for win in WINS]):
            win = list([win for win in WINS if win.issubset(game['X'])][0])
            print("X wins", win)
            game["turn"] = None
            game["winner"] = ("X", game["playerX"])
            game["win"] = win
        elif any([win.issubset(game['O']) for win in WINS]):
            win = list([win for win in WINS if win.issubset(game['O'])][0])
            print("O wins", win)
            game["turn"] = None
            game["winner"] = ("O", game["playerO"])
            game["win"] = win
        elif (len(game['X']) + len(game['O'])) == 9:
            game["turn"] = None
            game["winner"] = ("-", "🐈")    

        return game, 201
    
class GameList(Resource):
    def get(self):
        return list(GAMES.keys())

    def post(self):
        args = parser.parse_args()
        player = None
        if 'player' in args:
            player = args['player']
        # join a game if awaiting a player
        vacant_games = [game_id for game_id in GAMES if 'playerO' not in GAMES[game_id]]
        if vacant_games:
            game_id = vacant_games.pop()
            game = GAMES[game_id]
            if not player:
                player = "two"
            game['playerO'] = player
            #GAMES[game_id] = game 
            print(player, "joined game", game_id)
            return game, 201
        # otherwise create a game
        game_id = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        while game_id in GAMES:
            game_id = ''.join(random.choices(string.ascii_letters + string.digits, k=4))
        print(player, "created game", game_id)
        game = {"gameId": game_id, "playerX": player, "X": [], "O": [], "turn": "X"}
        GAMES[game_id] = game 
        return game, 201


api.add_resource(GameList, '/games')
api.add_resource(Game, '/games/<game_id>')

if __name__ == '__main__':
    app.run(debug=False)
