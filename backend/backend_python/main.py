from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware # Used to connect to frontend
from pydantic import BaseModel # Used for login/sign
from typing import Optional # Used for if query is not required
import uuid # Generates unique ID's for games
import json
import os
import datetime # Stores the data when games start

from board.go import Board  
from model.mct2 import MCTS
from utils.boardToTensor import boardToTensor
from model.net import GoNet
import numpy as np


from backend.backend_python.pvp import router as pvp_router


BOARD_SIZE = 9
GAMES_FILE = "saved_games.json"
USERS_FILE = "users.json"

app = FastAPI()

# Allow port on frontend to interact with this specific backend
# and use any request method.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StartGameRequest(BaseModel):
    opponent: str
    uid: str

class MoveRequest(BaseModel):
    x: int
    y: int

class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    email: str
    password: str

def load_json_file(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        except json.JSONDecodeError:
            pass

    # if file doesn't exist or invalid content, create empty file with []
    with open(filename, "w") as f:
        f.write("[]")
    return []


saved_games = load_json_file(GAMES_FILE)
users = load_json_file(USERS_FILE)

def save_games():
    with open(GAMES_FILE, "w") as f:
        json.dump(saved_games, f, indent=2)

def save_users():
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

game_state = {}
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


@app.post("/signup")
def signup(request: SignupRequest):

    # Prevents multiple accounts from sharing the same email.
    for user in users:
        if user["email"] == request.email:
            return {"success": False, "error": "User already exists"}
        
    users.append({"email": request.email, "password": request.password})
    save_users()
    return {"success": True}


@app.post("/login")
def login(request: LoginRequest):

    # Logins into account if it exist.
    for user in users:
        if user["email"] == request.email and user["password"] == request.password:
            return {"success": True}
        
    return {"success": False, "error": "Invalid email or password"}


@app.post("/newgame")
def new_game(request: StartGameRequest):

    # game_state is stores data for json.
    global game_state, board

    # Require uid to exist in users
    if not any(user["email"] == request.uid for user in users):
        raise HTTPException(status_code=400, detail="Invalid user")

    game_id = str(uuid.uuid4())
    board = Board(BOARD_SIZE)  # reset board

    game_state = {
        "game_id": game_id,
        "board": [[None]*BOARD_SIZE for _ in range(BOARD_SIZE)],
        "moves": [],
        "current_turn": "black",
        "opponent": request.opponent,
        "date": str(datetime.date.today()),
        "uid": request.uid,
        "winner": None,
    }

    return {"board": game_state["board"], "game_id": game_id, "opponent": request.opponent}


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
    mct = MCTS(network=network, exploration_weight=1.5, simulations=800)

    move_ai, _ = mct.search(board)

    if move_ai is None or move_ai == 81:
        # AI pass move, implement pass logic if needed
        game_state["winner"] = "black"  # simplistic winner on pass
    else:
        ai_x, ai_y = divmod(move_ai, BOARD_SIZE)
        board.playMove(ai_x, ai_y, -1)  # -1 = white
        game_state["board"][ai_y][ai_x] = "white"
        game_state["moves"].append({"player": "white", "x": ai_x, "y": ai_y})

    mct.update_root(move_ai)

    # Save or update saved_games for this user
    for g in saved_games:
        if g["game_id"] == game_state["game_id"]:
            g.update({
                "board": game_state["board"],
                "moves": game_state["moves"],
                "winner": game_state.get("winner"),
            })
            break
    else:
        saved_games.append(game_state.copy())

    save_games()

    return numpy_array_to_json(board)


@app.get("/stats")
def get_stats(uid: Optional[str] = Query(None)):
    # Filter games by uid (user email)
    if uid:
        user_games = [g for g in saved_games if g.get("uid") == uid]
    else:
        user_games = []
    return user_games


