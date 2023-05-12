# Tic-Tac-Toe 

```python
headers = {"Content-Type": "application/json"}
```

## Messages

POST /game/
```
{
    "id": "123",
    "X": [],
    "O": [],
    "status": "X_PLAY"
}

PUT /game/:id
```
{
    "id": "123",
    "X": 22
}
```

GET /game/:id

```
{
    "id": "123",
    "X": [11,13,22,31,33],
    "O": [12,21,23,32],
    "status": "X_WON"
}
```
