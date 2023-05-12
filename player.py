import sys
import time

from requests import get, post, put
from random import choice

GAME_URL = "http://localhost:5000"
headers = {"Content-Type": "application/json"}

MOVES = [0,1,2,10,11,12,20,21,22]

def result(game):
    if 'winner' in game:
        print("winner!",game['winner'])
    print(game)
    for r in range(3):
        for c in range(3):
            pos = r*10+c
            if pos in game['X']:
                print("X ",end='')
            elif pos in game['O']:
                print("O ",end='')
            else:
                print("- ",end='')
        print()

def play(piece, game):
    while 'winner' not in game and (len(game['X']) + len(game['O']) < 9):
        foo = get(GAME_URL+"/games/"+game['gameId'], headers=headers)
        game = foo.json()
        if game['turn'] == piece:
            my_play = choice(MOVES)
            while my_play in game['X'] or my_play in game['O']:
                 my_play = choice(MOVES)
            move = {game["turn"]: my_play}
            print("playing", move)
            play = put(GAME_URL+"/games/"+game['gameId'], headers=headers, json=move)
            if play.status_code//100 == 4:
                print(play.status_code, play.json())
        time.sleep(3)
    result(game)


def start(player):
    foo = post(GAME_URL+"/games", json={"player": player}, headers=headers)
    if foo.status_code//100 != 2:
        print(foo.status_code, foo.json())
        return
    game = foo.json()
    piece = None
    if 'playerX' in game and game['playerX'] == player:
        piece = 'X'
    elif 'playerO' in game and game['playerO'] == player:
        piece = 'O'
    else:
        print("unexpected start", game)
        return
    play(piece, game)



def main(argv):
    if len(argv) < 2:
        print("Usage: {} <name>".format(argv[0]))
    else:
        start(argv[1])

if __name__ == '__main__':
    main(sys.argv)