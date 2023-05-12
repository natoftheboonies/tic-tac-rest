from requests import get, post, put
from random import choice

GAME_URL = "http://localhost:5000"
headers = {"Content-Type": "application/json"}

foo = get(GAME_URL+"/games", headers=headers)
print(foo.status_code, foo.json())

# player one joins a game
foo = post(GAME_URL+"/games", json={"player": "nat"}, headers=headers)
print(foo.status_code, foo.json())

# player two joins a game
foo = post(GAME_URL+"/games", json={"player": "alex"}, headers=headers)
print(foo.status_code, foo.json())
game = foo.json()

# play randomly, including invalid move (36)
MOVES = [0,1,2,10,11,12,20,21,22,36]
for _ in range(50):
    if not game["turn"]: 
        break
    my_play = choice(MOVES)
    #MOVES.remove(my_play)
    move = {game["turn"]: my_play}
    print("playing", move)
    play = put(GAME_URL+"/games/"+game['gameId'], headers=headers, json=move)
    if play.status_code//100 == 4:
        print(play.status_code, play.json())
    foo = get(GAME_URL+"/games/"+game['gameId'], headers=headers)
    # print(foo.status_code, foo.json())    
    game = foo.json()

print("winner!",game['winner'])
print(game)

# print the match result
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