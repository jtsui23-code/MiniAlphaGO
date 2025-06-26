from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from predict import getBestMove

app = FastAPI()

class BoardState(BaseModel):
    board: List[List[int]]  # 9x9 board with 1 (black), -1 (white), 0 (empty)

@app.post("/predict")
async def predict_move(state: BoardState):
    """
    Expects JSON payload:
    {
        "board": [
            [0, 0, 1, ..., 0],
            ...,
            [0, -1, 0, ..., 0]
        ]
    }

    Returns:
    {
        "move": int  # Flattened index (0-80) representing the model's chosen move
    }
    """
    x, y = getBestMove(state.board)
    move_index = x * 9 + y  # Convert (x, y) to single index for frontend
    return {"move": move_index}
