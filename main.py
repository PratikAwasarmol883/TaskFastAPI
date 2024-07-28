from fastapi import FastAPI
from routers.task import router as TaskRouter
app = FastAPI()

app.include_router(TaskRouter)