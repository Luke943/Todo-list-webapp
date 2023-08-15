from fastapi import FastAPI
from pydantic import BaseModel


class Todo(BaseModel):
    id: int
    task: str
