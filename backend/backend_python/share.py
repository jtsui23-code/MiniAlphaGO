import json
import os
import numpy as np

BOARD_SIZE = 9
GAMES_FILE = "saved_games.json"
USERS_FILE = "users.json"

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

def load_json_file(filename):
    if os.path.exists(filename):
        try:
            with open(filename, "r") as f:
                content = f.read().strip()
                if content:
                    return json.loads(content)
        except json.JSONDecodeError:
            pass
    with open(filename, "w") as f:
        f.write("[]")
    return []

def save_games():
    with open(GAMES_FILE, "w") as f:
        json.dump(saved_games, f, indent=2)
    


saved_games = load_json_file(GAMES_FILE)
users = load_json_file(USERS_FILE)