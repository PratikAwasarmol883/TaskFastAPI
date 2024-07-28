from fastapi import APIRouter, HTTPException
from starlette import status
from fastapi.responses import HTMLResponse
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session
from models import Task
from fastapi import Depends, Request
from pydantic import BaseModel, Field

models.Base.metadata.create_all(bind=engine)
from routers.request import RequestTask


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


router = APIRouter(
    prefix="/task",
    tags=["task"]
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_task(db: Session = Depends(get_db)):
    task_model = db.query(Task).all()
    return task_model


@router.get("/task/{task_id}", status_code=status.HTTP_200_OK)
async def get_task_by_id(task_id: str, db: Session = Depends(get_db)):
    task_model = db.query(Task).filter(Task.id == task_id).first()
    if task_model is not None:
        return task_model
    raise HTTPException(status_code=404, detail="Task Id Not Found: ")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_task(request_task: RequestTask, db: Session = Depends(get_db)):
    task_model = Task(**request_task.model_dump())
    db.add(task_model)
    db.commit()


@router.put("/task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_task(request_task: RequestTask, task_id: int, db: Session = Depends(get_db)):
    task_model = db.query(Task).filter(Task.id == task_id).first()
    if task_model is None:
        raise HTTPException(status_code=404, detail="Task id not found.")

    task_model.taskName = request_task.taskName
    task_model.whatYouLearnt = request_task.whatYouLearnt
    db.add(task_model)
    db.commit()

    return {"message": "Task updated successfully"}


@router.delete("/task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id:int, db: Session = Depends(get_db)):
    task_model = db.query(Task).filter(Task.id == task_id).first()
    if task_model is None:
        raise HTTPException(status_code=404, detail="Task id not found.")
    db.query(Task).filter(Task.id == task_id).delete()
    db.commit()
    return {"message": "Task updated successfully"}