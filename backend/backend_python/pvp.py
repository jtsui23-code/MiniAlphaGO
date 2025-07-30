from fastapi import APIRouter, HTTPException, Query
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

from backend.backend_python.share import users
from backend.backend_python.share import save_games
from backend.backend_python.share import saved_games
from backend.backend_python.share import numpy_array_to_json



GAME_FILES = "saved_games.json"
BOARD_SIZE = 9

# game_state = {}
# board = Board(BOARD_SIZE)
pvp_games = {}

class StartPvP(BaseModel):
    uid: str    # User id that made the game.

class JoinPvp(BaseModel):
    uid: str

class PvpMove(BaseModel):
    uid: str
    x: int
    y: int
    passTurn: bool



router = APIRouter()

def generateInviteCode(length=6):
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


@router.post("/pvpStart")
def start_pvp(request:StartPvP):

    global pvp_games
    if not any (user["email"] == request.uid for user in users):
        raise HTTPException(status_code=400, detail="Invalid user")
    
    game_id = str(uuid.uuid4())
    board = Board(BOARD_SIZE)
    inviteCode = generateInviteCode(6)
    # inviteCode = "Test123"

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
        "inviteCode": inviteCode,
        "board_obj": board
    }


    pvp_games[inviteCode] = game_state


    return {"board": game_state["board"], "game_id": game_id, "invite_code": inviteCode}


@router.post("/join")
def joinPvp(request: JoinPvp, inviteCode: Optional[str] = Query(None)):
    
    global pvp_games

    if inviteCode not in pvp_games:
        raise HTTPException(status_code=400, detail="Invalid or missing game_id")
    
    if pvp_games[inviteCode]["opponent"] != None:
        raise HTTPException(status_code=400, detail="Game is full")

    if request.uid == pvp_games[inviteCode]["uid"]:
        raise HTTPException(status_code=400, detail="Cannot be the opponent of your own game")


    pvp_games[inviteCode]["opponent"] = request.uid

    return {"Success": True}



@router.put("/pvpMove")
def pvp_move(move :PvpMove, inviteCode: Optional[str] = Query(None)):
    
    global pvp_games

    if inviteCode not in pvp_games:
        raise HTTPException(status_code=400, detail="Game doesn't exist")

    if pvp_games[inviteCode]["opponent"] is None:
        raise HTTPException(status_code=400, detail="No opponent to start game.")


    x, y, passTurn = move.x, move.y, move.passTurn

    player1 = pvp_games[inviteCode]["uid"]
    player2 = pvp_games[inviteCode]["opponent"]

    if passTurn != True:
        if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
            raise HTTPException(status_code=400, detail="Move out of board bounds")

        if pvp_games[inviteCode]["board"][y][x] is not None:
            raise HTTPException(status_code=400, detail="Cell already occupied")
    


    if pvp_games[inviteCode]["current_turn"] == "black" and move.uid == player1:



        if passTurn:

            pvp_games[inviteCode]["board_obj"].playMove(1,1, 1, passTurn=True)
            pvp_games[inviteCode]["current_turn"] = "white"
            pvp_games[inviteCode]["moves"].append({"player": "black", "x": None, "y": None, "pass": True})

            return numpy_array_to_json(pvp_games[inviteCode]["board_obj"])




        pvp_games[inviteCode]["board_obj"].playMove(x,y, 1)
        pvp_games[inviteCode]["board"][y][x] = "black"
        pvp_games[inviteCode]["moves"].append({"player": "black", "x": x, "y": y})

        pvp_games[inviteCode]["current_turn"] = "white"


    elif pvp_games[inviteCode]["current_turn"] == "white" and move.uid == player2:



        if passTurn:

            pvp_games[inviteCode]["board_obj"].playMove(1,1, -1, passTurn=True)
            pvp_games[inviteCode]["current_turn"] = "black"
            pvp_games[inviteCode]["moves"].append({"player": "white", "x": None, "y": None, "pass": True})

            return numpy_array_to_json(pvp_games[inviteCode]["board_obj"])




        pvp_games[inviteCode]["board_obj"].playMove(x,y, -1)
        pvp_games[inviteCode]["board"][y][x] = "white"
        pvp_games[inviteCode]["moves"].append({"player": "white", "x": x, "y": y})

        pvp_games[inviteCode]["current_turn"] = "black"


    else:
        raise HTTPException(status_code=400, detail="Not your turn to play")



    for game in saved_games:
        if game["game_id"] == pvp_games[inviteCode]["game_id"]:
            game.update({
                "board": pvp_games[inviteCode]["board"],
                "moves": pvp_games[inviteCode]["moves"],
                "winner": pvp_games[inviteCode].get("winner")
            })
            break


    else:

        # Appending a copy of the game object without the
        # board object because its non-serializable because its a class
        # so JSON can't save it.
        game_copy = pvp_games[inviteCode].copy()
        del game_copy["board_obj"]
        saved_games.append(game_copy)

    save_games()

    return numpy_array_to_json(pvp_games[inviteCode]["board_obj"])









    


    




