from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials, auth, initialize_app
from typing import List
from pydantic import BaseModel
import datetime

game_data = {}

cred = credentials.Certificate("serviceAccountKey.json")
initialize_app(cred)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust to your frontend origin in production
    allow_methods=["*"],
    allow_headers=["*"],
)

class GameRecord(BaseModel):
    opponent: str
    result: str
    moves: List[str]
    date: str

@app.get("/stats")
async def get_stats(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    id_token = auth_header.split(" ")[1]

    try:
        decoded = auth.verify_id_token(id_token)
        uid = decoded["uid"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"games": game_data.get(uid, [])}


@app.post("/record_game")
async def record_game(request: Request):
    body = await request.json()
    id_token = body.get("idToken")

    try:
        decoded = auth.verify_id_token(id_token)
        uid = decoded["uid"]
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid Firebase token")

    game = {
        "opponent": body.get("opponent", "AI"),
        "result": body.get("result", "Win"),
        "moves": body.get("moves", []),
        "date": datetime.datetime.now().strftime("%Y-%m-%d"),
    }

    if uid not in game_data:
        game_data[uid] = []
    game_data[uid].append(game)

    return {"success": True}
