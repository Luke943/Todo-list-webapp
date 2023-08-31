from typing import Optional

from pydantic import BaseModel


class TodoItemBase(BaseModel):
    text: str


class TodoItemCreate(TodoItemBase):
    pass


class TodoItem(TodoItemBase):
    id: int
    done: bool
    owner_id: int

    class Config:
        from_attributes = True


class TodoItemUpdate(BaseModel):
    text: Optional[str] = None
    done: Optional[bool] = None
    owner_id: Optional[int] = None


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    is_active: bool
    items: list[TodoItem] = []

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    is_active: Optional[bool] = None
