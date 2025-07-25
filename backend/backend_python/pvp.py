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



import random 
import string
from backend.backend_python.main import MoveRequest
from backend.backend_python.main import users

GAME_FILES = "saved_games.json"
BOARD_SIZE = 9

game_state = {}
board = Board(BOARD_SIZE)
pvp_games = {}

class StartPvP(BaseModel):
    uid: str    # User id that made the game.

class JoinPvp(BaseModel):
    uid: str



app = FastAPI()

def generateInviteCode(length=6):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


@app.post("/pvpStart")
def start_pvp(request:StartPvP):

    global game_state, board, pvp_games
    if not any (user["email"] == request.uid for user in users):
        raise HTTPException(status_code=400, detail="Invalid user")
    
    game_id = str(uuid.uuid4())
    board = Board(BOARD_SIZE)
    inviteCode = generateInviteCode(6)

    game_state = {
        "game_id": game_id,
        # Fills 2D array with Nones
        "board": [[None]*BOARD_SIZE for _ in range(BOARD_SIZE)],
        "moves": [],
        "current_turn": "black",
        "opponent": None,
        "date": str(datetime.date.today()),
        "uid": request.uid,
        "winner": None,
        "inviteCode": inviteCode
    }

    pvp_games[inviteCode] = game_state


    return {"board": game_state["board"], "game_id": game_id}


@app.post("/join")
def joinPvp(request: JoinPvp, inviteCode: Optional[str] = Query(None)):
    
    global game_state, board

    if inviteCode != game_state.get("inviteCode"):
        raise HTTPException(status_code=400, detail="Invalid or missing game_id")
    
    if game_state["opponent"] != None:
        raise HTTPException(status_code=400, detail="Game is full")

    if request.uid == game_state.get("uid"):
        raise HTTPException(status_code=400, detail="Cannot be the opponent of your own game")


    game_state["opponent"] = request.uid

    return {"Success": True}

@app.put("pvpMove")
def pvp_move(move :MoveRequest, game_id: Optional[str] = Query(None)):
    
    global game_state, pvp_games, board

    if game_id != game_state.get("game_id"):
        raise HTTPException(status_code=400, detail="Invalid or missing game_id")

    x, y = move.x, move.y

    


    


    




