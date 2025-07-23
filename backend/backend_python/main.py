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
ACCOUNTS_FILE = "accounts.json"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Account storage init
if not os.path.exists(ACCOUNTS_FILE):
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump({}, f)

# Game storage init
if os.path.exists(GAMES_FILE):
    with open(GAMES_FILE, "r") as f:
        saved_games = json.load(f)
else:
    saved_games = []

def save_games():
    with open(GAMES_FILE, "w") as f:
        json.dump(saved_games, f)

# Models
class StartGameRequest(BaseModel):
    opponent: str
    uid: Optional[str]  # user email from frontend

class MoveRequest(BaseModel):
    x: int
    y: int

class User(BaseModel):
    email: str
    password: str

# Account endpoints
@app.post("/signup")
def signup(user: User):
    with open(ACCOUNTS_FILE, "r") as f:
        accounts = json.load(f)
    if user.email in accounts:
        return {"error": "Email already exists"}
    accounts[user.email] = user.password
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f)
    return {"success": True}

@app.post("/login")
def login(user: User):
    with open(ACCOUNTS_FILE, "r") as f:
        accounts = json.load(f)
    if accounts.get(user.email) != user.password:
        return {"error": "Invalid credentials"}
    return {"success": True}

# Game state global variables
game_state = {}
board = Board(BOARD_SIZE)
opponent_counter = 0

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

# Start new game
@app.post("/newgame")
def new_game(request: StartGameRequest):
    global game_state, opponent_counter, board

    if not request.uid:
        raise HTTPException(status_code=400, detail="User ID required")

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
        "user": request.uid,
    }

    return {"board": game_state["board"], "game_id": game_id, "opponent": opponent_name}

# Make move
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

    # Player move (black)
    board.playMove(x, y, 1)
    game_state["board"][y][x] = "black"
    game_state["moves"].append({"player": "black", "x": x, "y": y})

    # AI move
    network = GoNet(9, 17)
    mct = MCTS(network=network, exploration_weight=1.5, simulations=500)
    move_ai, _ = mct.search(board)

    if move_ai is None or move_ai == 81:
        pass  # AI pass logic if needed
    else:
        ai_x, ai_y = divmod(move_ai, BOARD_SIZE)
        board.playMove(ai_x, ai_y, -1)
        game_state["board"][ai_y][ai_x] = "white"
        game_state["moves"].append({"player": "white", "x": ai_x, "y": ai_y})

    mct.update_root(move_ai)

    # Save/update saved_games with user info
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

# Fetch stats filtered by user (query param)
@app.get("/stats")
def get_stats(user: Optional[str] = None):
    if not user:
        return []

    user_games = [g for g in saved_games if g.get("user") == user]
    return user_games
