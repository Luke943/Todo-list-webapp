"""
Older version of the app without browser interface
"""

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


"""
Root
"""


@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}


"""
Users
"""


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists"
        )
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db=db, skip=skip, limit=limit)


@app.get("/users/{user_id}/", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


@app.put("/users/{user_id}/", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db=db, user_id=user_id, user=user)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


@app.delete("/users/{user_id}/", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return db_user


"""
Todo Items
"""


@app.post("/users/{user_id}/items/", response_model=schemas.TodoItemCreate)
def create_todoitem_for_user(
    user_id: int, item: schemas.TodoItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_todoitem(db=db, item=item, user_id=user_id)


@app.get("/items/", response_model=list[schemas.TodoItem])
def read_todoitems(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_todoitems(db=db, skip=skip, limit=limit)


@app.put("/items/{item_id}/", response_model=schemas.TodoItem)
def update_todoitem(
    item_id: int, item: schemas.TodoItemUpdate, db: Session = Depends(get_db)
):
    db_item = crud.update_todoitem(db=db, item_id=item_id, item=item)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found"
        )
    return db_item


@app.delete("/items/{item_id}/", response_model=schemas.TodoItem)
def delete_todoitem(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_todoitem(db=db, item_id=item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found"
        )
    return db_item
