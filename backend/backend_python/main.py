from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid
import json
import os
import datetime

from board.go import Board  
from model.mct2 import MCTS
from utils.boardToTensor import boardToTensor
from model.net import GoNet
import numpy as np

BOARD_SIZE = 9
GAMES_FILE = "saved_games.json"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class StartGameRequest(BaseModel):
    opponent: str

class MoveRequest(BaseModel):
    x: int
    y: int

if os.path.exists(GAMES_FILE):
    with open(GAMES_FILE, "r") as f:
        saved_games = json.load(f)
else:
    saved_games = []

def save_games():
    with open(GAMES_FILE, "w") as f:
        json.dump(saved_games, f)

game_state = {}
opponent_counter = 0
board = Board(BOARD_SIZE)

def numpy_array_to_json(arr):
    if not isinstance(arr, np.ndarray):
        if hasattr(arr, 'board'):
            arr = arr.board
        else:
            arr = np.array(arr)

    def convert_val(val):
        if isinstance(val, float) and np.isnan(val):
            return None
        if val == -1:
            return "white"
        if val == 1:
            return "black"
        if val == 0:
            return None
        if hasattr(val, 'item'):
            return val.item()
        return val

    nested_list = [[convert_val(v) for v in col] for col in arr.T]
    return nested_list

@app.post("/newgame")
def new_game(request: StartGameRequest):
    global game_state, opponent_counter, board
    opponent_counter += 1
    opponent_name = f"{request.opponent} v{opponent_counter}"

    game_id = str(uuid.uuid4())
    board = Board(BOARD_SIZE)  # reset board

    game_state = {
        "game_id": game_id,
        "board": [[None]*BOARD_SIZE for _ in range(BOARD_SIZE)],
        "moves": [],
        "current_turn": "black",
        "opponent": opponent_name,
        "date": str(datetime.date.today()),
    }

    return {"board": game_state["board"], "game_id": game_id, "opponent": opponent_name}

@app.put("/move")
def make_move(move: MoveRequest, game_id: Optional[str] = Query(None)):
    global game_state, saved_games, board

    if game_id != game_state.get("game_id"):
        raise HTTPException(status_code=400, detail="Invalid or missing game_id")

    x, y = move.x, move.y

    if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
        raise HTTPException(status_code=400, detail="Move out of board bounds")

    if game_state["board"][y][x] is not None:
        raise HTTPException(status_code=400, detail="Cell already occupied")

    # Player (black) move on backend Board object and game_state
    board.playMove(x, y, 1)  # 1 = black
    game_state["board"][y][x] = "black"
    game_state["moves"].append({"player": "black", "x": x, "y": y})

    # AI move with MCTS
    network = GoNet(9, 17)
    mct = MCTS(network=network, exploration_weight=1.5, simulations=500)

    move_ai, _ = mct.search(board)

    if move_ai is None or move_ai == 81:
        # AI pass move, implement pass logic if needed
        pass
    else:
        ai_x, ai_y = divmod(move_ai, BOARD_SIZE)
        board.playMove(ai_x, ai_y, -1)  # -1 = white
        game_state["board"][ai_y][ai_x] = "white"
        game_state["moves"].append({"player": "white", "x": ai_x, "y": ai_y})

    mct.update_root(move_ai)

    # Save or update saved_games
    for g in saved_games:
        if g["game_id"] == game_state["game_id"]:
            g.update({
                "board": game_state["board"],
                "moves": game_state["moves"],
            })
            break
    else:
        saved_games.append(game_state.copy())

    save_games()

    return numpy_array_to_json(board)

@app.get("/stats")
def get_stats():
    return saved_games
