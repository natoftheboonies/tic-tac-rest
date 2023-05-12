from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

GAME = {"id": 123,
        "X": [],
        "O": [],
        "turn": "X"}

def abort_if_todo_doesnt_exist(game_id):
    if game_id != GAME["id"]:
        abort(404, message="Game {} doesn't exist".format(game_id))

parser = reqparse.RequestParser()
parser.add_argument('X')
parser.add_argument('O')

class Game(Resource):

    def state(self, game_id):
        return GAME

    def get(self, game_id):
        abort_if_todo_doesnt_exist(game_id)
        return GAME

    def put(self, game_id):
        args = parser.parse_args()
        if GAME["turn"] == "X" and args['X']:
            GAME["X"].append(int(args['X']))
            GAME["turn"] = "O"
        elif GAME["turn"] == "O" and args['O']:
            GAME["O"].append(int(args['O']))
            GAME["turn"] = "X"
        return GAME, 201
    
class GameList(Resource):
    def get(self):
        return GAME

    def post(self):
        args = parser.parse_args()
        return GAME, 201


api.add_resource(GameList, '/games')
api.add_resource(Game, '/games/<game_id>')


if __name__ == '__main__':
    app.run(debug=True)
