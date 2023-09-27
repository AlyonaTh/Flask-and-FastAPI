import uvicorn
from typing import Optional

from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel, EmailStr

app = FastAPI()


class NewTask(BaseModel):
    title: str
    description: Optional[str]
    status: str


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: str


tasks = []


@app.get("/tasks", response_model=list[Task])
async def get_tasks():
    return tasks


@app.get("/tasks/{item_id}", response_model=Task)
async def get_item_by_id(item_id: int):
    task = [task for task in tasks if task.id == item_id]
    if task:
        return task[0]
    raise HTTPException(status_code=404, detail="Task not found")


@app.post("/tasks/", response_model=Task)
@app.post("/tasks/")
async def create_task(task: NewTask):
    new_id = 1
    if tasks:
        new_id = max(tasks, key=lambda x: x.id).id + 1
    if task.status.lower() not in ["todo", "in progress", "done"]:
        return {"message": f"Wrong status: '{task.status}'\nOnly 'tоdo', 'in progress' or 'done' statuses available."}
    tasks.append(added_task := Task(
        id=new_id,
        title=task.title.capitalize(),
        description=task.description.capitalize(),
        status=task.status.lower(),
    ))
    return added_task


@app.put("/tasks/{task_id}", response_model=Task)
@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task: Task):
    upd_task = [t for t in tasks if t.id == task_id]
    if not upd_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status.lower() not in ["todo", "in progress", "done"]:
        return {"message": f"Wrong status: '{task.status}'\nOnly 'tоdo', 'in progress' or 'done' statuses available."}
    upd_task[0].title = task.title.capitalize()
    upd_task[0].description = task.description.capitalize()
    upd_task[0].status = task.status.lower()
    return upd_task


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    del_task = [t for t in tasks if t.id == task_id]
    if not del_task:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks.remove(del_task[0])
    return del_task[0]


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )