from fastapi import FastAPI  # Fix typo here

app = FastAPI()

users = ["bobby", "don", "bob"]
items = []

@app.get("/")
def root():
    return {"Hello": "World"}

@app.post("/items")
def create_item(item: str):
    items.append(item)
    return items

@app.get("/items/{item_id}")  # Fix path syntax
def get_item(item_id: int) -> str:
    return items[item_id]

@app.get("/users/{user_id}")
def get_user(user_id: int) -> str:
    return users[user_id]

@app.post("/users")
def post_user(user: str):
    users.append(user)
    return users