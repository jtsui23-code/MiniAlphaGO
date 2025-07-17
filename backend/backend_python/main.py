from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

app = FastAPI()

origins = [
    "http://localhost:3000",  # React dev server origin
    "http://localhost:8000",  # Same origin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BOARD_SIZE = 9

class StartGameRequest(BaseModel):
    opponent: str

class MoveRequest(BaseModel):
    x: int
    y: int
    player: str

# Store board in memory for demo purposes
game_state = {
    "board": [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)],
    "current_turn": "black",
}

@app.post("/newgame")
def new_game(request: StartGameRequest):
    # Reset the board and current turn
    game_state["board"] = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    game_state["current_turn"] = "black"
    print(f"New game started against opponent: {request.opponent}")
    return game_state["board"]

@app.put("/move")
def make_move(move: MoveRequest):
    x, y, player = move.x, move.y, move.player

    # Validate coordinates
    if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
        raise HTTPException(status_code=400, detail="Move out of board bounds")

    # Validate player
    if player not in ("black", "white"):
        raise HTTPException(status_code=400, detail="Invalid player")

    # Check if it's this player's turn
    if player != game_state["current_turn"]:
        raise HTTPException(status_code=400, detail=f"Not {player}'s turn")

    # Check if the cell is empty
    if game_state["board"][y][x] is not None:
        raise HTTPException(status_code=400, detail="Cell is already occupied")

    # Make the move
    game_state["board"][y][x] = player

    # Swap turns
    game_state["current_turn"] = "white" if player == "black" else "black"

    # Return updated board (frontend can track turns itself)
    return game_state["board"]
