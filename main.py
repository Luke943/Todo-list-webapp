from fastapi import FastAPI, HTTPException
from models import Todo

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to my fastapi example"}


todos: list[Todo] = []


# Get all todos
@app.get("/todos")
async def get_todos():
    return {"todos": todos}


# Get single todo
@app.get("/todos/{item_id}")
async def get_todo(item_id: int):
    for x in todos:
        if x.id == item_id:
            return {"todo": x}
    raise HTTPException(status_code=404, detail="Item not found")


# Create a todo
@app.post("/todos")
async def create_todos(todo: Todo):
    todos.append(todo)
    return {"message": "Todo has been added"}


# Update a todo
@app.put("/todos/{item_id}")
async def update_todo(item_id: int, todo: Todo):
    if todo.id != item_id:
        raise HTTPException(status_code=400, detail="id's do not match")
    for x in todos:
        if x.id == item_id:
            x.task = todo.task
            return {"message": "Todo has been changed"}
    raise HTTPException(status_code=404, detail="Item not found")


# Delete a todo
@app.delete("/todos/{item_id}")
async def delete_todo(item_id: int):
    for x in todos:
        if x.id == item_id:
            todos.remove(x)
            return {"message": "Todo has been deleted"}
    raise HTTPException(status_code=404, detail="Item not found")
