# Tic-Tac-Toe

This demonstrates a client-server Tic-Tac-Toe game.

To make it go:

1. Start the server with `python game.py` and then open http://localhost:5000/static/index.html in a browser.
2. in another terminal, start a player with `python player.py Alice` or similar.
3. reload the browser to start following this game.
4. in a third terminal, start a player with `python player.py Bob` or similar.
5. watch Alice and Bob battle in the browser.
6. to play it again, restart at #2.

## Server

- `game.py` is the server, providing RESTful APIs. It can handle concurrent games, I think.

## Clients

- `testgame.py` will play both players, including illegal guesses.
- `player.py` will play a single player, waiting a few seconds between API calls.

## Monitor

- `static/index.html` will ask the server for a game, and start following the latest one. Inspect the javascript to see how.

## Messages

You can see a list of the `gameId`s that the server knows about by asking:

- GET /games

This returns a list, like `['rrQw', 'oRAH']`

To start or join a game, send a message indicating your `player` name.

- POST /games

request:

```json
{ "player": "nat" }
```

response:

```json
{
  "gameId": "rrQw",
  "playerX": "nat",
  "playerY": "alex",
  "X": [],
  "O": [],
  "turn": "X"
}
```

You will be `playerX` or `playerY` and maybe it is your `turn` to play!

You can check the status of a game by asking via GET

- GET /games/:game_id

```json
{
  "gameId": "rrQw",
  "X": [10, 12, 21, 22],
  "O": [0, 20, 2, 1],
  "playerX": "nat",
  "playerO": "alex",
  "turn": null,
  "winner": ["O", "alex"],
  "win": [0, 1, 2]
}
```

To play a move, send a PUT message to `/games/game_id` with your play.

- PUT /games/:game_id

You will get an error 401 if you try to play when it is not your turn, or try to overwrite an prior play.

request:

```json
{ "X": 22 }
```

valid plays are numbers from the board:

```
[ 0, 1, 2]
[10,11,12]
[20,21,22]
```
