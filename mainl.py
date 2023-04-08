from fastapi import FastAPI, HTTPException

app = FastAPI()
todos = []

@app.post("/todos")
async def add_todo(item: str):
    todos.append(item)
    return {"id": len(todos) - 1, "item": item}

@app.get("/todos")
async def get_todos():
    return {"todos": todos}

@app.delete("/todos/{id}")
async def delete_todo(id: int):
    if id < 0 or id >= len(todos):
        raise HTTPException(status_code=404, detail="Todo not found")
    todos.pop(id)
    return {"status": "success"}
