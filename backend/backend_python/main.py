from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

from board.go import Board  
from model.mct2 import MCTS
from utils.boardToTensor import boardToTensor
from  model.net import GoNet

import numpy as np
import json

import numpy as np
import json

import numpy as np
import json

import numpy as np

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

    # Transpose to flip X and Y
    nested_list = [[convert_val(v) for v in col] for col in arr.T]
    return nested_list



board = Board(9)

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

    global board
    board = Board(9)

    return game_state["board"]

@app.put("/move")
def make_move(move: MoveRequest):
    Zx, Zy = move.x, move.y


    # Make the move
    #game_state["board"][y][x] = player

    ## AI MAKES HIS MOVE
    global board
    board = AiMove(board,Zx,Zy)

    
        # Validate coordinates
    #if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
     #   raise HTTPException(status_code=400, detail="Move out of board bounds")

    # Validate player
    #if player not in ("black", "white"):
     #   raise HTTPException(status_code=400, detail="Invalid player")

    # Check if it's this player's turn
    #if player != game_state["current_turn"]:
     #   raise HTTPException(status_code=400, detail=f"Not {player}'s turn")

    # Check if the cell is empty
    #if game_state["board"][y][x] is not None:
        #raise HTTPException(status_code=400, detail="Cell is already occupied")
    

    # Swap turns
    #game_state["current_turn"] = "white" if player == "black" else "black"

    # Return updated board (frontend can track turns itself)
    return numpy_array_to_json(board)


def AiMove(board,Zx,Zy):
    # Gets the best move and the pi vector which is the probability of all the moves.
        network = GoNet(9,17)
        mct = MCTS(network=network,exploration_weight=1.5, simulations=500)


        board.playMove(Zx,Zy,1)
        print(Zx, Zy)
        move, pi = mct.search(board)

        # Converts the board into a tensor which is the expected form for saving the gameData.
        # boardState = boardToTensor(board).to(device)

        boardState = boardToTensor(board)

        # 0 - 80 are the only valid moves on a 9x9 board. Move 81 is set to being a pass.
        if move is None or move == 81:
            print("AI passed")
            # Player passes if that is the move choosen by the mct.
            board.playMove(1,1, -1, passTurn=True)
        else:
            # Converting move which is a single int representation of the board position into 
            # a row and col representation of the 9x9 board.
            x, y = divmod(move, 9)
            
            # Playing the move choosen by the mct.
            board.playMove(x,y, -1)

            print(f"Player played at ", {x}, {y}, " position on the board")


        # Saves the game data each turn. 
        mct.update_root(move)


        return board