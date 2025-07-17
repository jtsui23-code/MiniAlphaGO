from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BOARD_SIZE = 9  # ← changed from 19
board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

class StartGameRequest(BaseModel):
    opponent: str

@app.post("/newgame")
def new_game(request: StartGameRequest):
    global board
    board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    print(f"New game vs {request.opponent}")
    return board

class Move(BaseModel):
    x: int
    y: int
    player: str

@app.put("/move")
def make_move(move: Move):
    global board
    if board[move.y][move.x] is not None:
        return {"error": "Invalid move: cell occupied"}
    
    board[move.y][move.x] = move.player
    return board
