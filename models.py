from database import Base
from sqlalchemy import Column, Integer, Boolean, String
from sqlalchemy.orm import relationship


class Task(Base):
    __tablename__ = "TaskList"
    id = Column(Integer,primary_key=True,unique=True)
    taskName = Column(String,unique=True)
    whatYouLearnt = Column(String)
