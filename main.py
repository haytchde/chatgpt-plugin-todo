from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel

app = FastAPI()


class Todo(BaseModel):
    id: int
    task: str


todos = []


@app.get("/todos", response_model=List[Todo])
async def get_todos():
    return todos


@app.post("/todos", response_model=Todo)
async def create_todo(todo: Todo):
    todos.append(todo)
    return todo


@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    todo_to_delete = None
    for todo in todos:
        if todo.id == todo_id:
            todo_to_delete = todo
            break
    if todo_to_delete:
        todos.remove(todo_to_delete)
        return {"status": "success", "message": "Todo deleted."}
    else:
        raise HTTPException(status_code=404, detail="Todo not found.")


@app.get("/.well-known/ai-plugin.json", include_in_schema=False)
async def ai_plugin():
    import json
    with open("manifest.json", "r") as f:
        manifest = json.load(f)
    return manifest

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
