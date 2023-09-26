from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")
templates = Jinja2Templates(directory="templates")


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
def read_root(request: Request, db: Session = Depends(get_db)):
    return RedirectResponse(url="/login/")


@app.get("/login/", response_class=HTMLResponse)
def read_login(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/register/", response_class=HTMLResponse)
def read_register(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/login/{username}", response_class=RedirectResponse)
def login_user(username: str, request: Request, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db=db, username=username)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return RedirectResponse(url=f"/users/{db_user.id}/items/")


"""
Users
"""


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    return crud.create_user(db=db, user=user)


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_users(db=db, skip=skip, limit=limit)


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db=db, user_id=user_id, user=user)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db=db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


"""
Todo Items
"""


@app.post("/users/{user_id}/items/", response_model=schemas.TodoItemCreate)
def create_todoitem_for_user(
    user_id: int, item: schemas.TodoItemCreate, db: Session = Depends(get_db)
):
    return crud.create_user_todoitem(db=db, item=item, user_id=user_id)


@app.get("/users/{user_id}/items/", response_class=HTMLResponse)
def read_todoitems_for_user(
    request: Request,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    todo_items = crud.get_user_todoitems(db=db, user_id=user_id, skip=skip, limit=limit)
    return templates.TemplateResponse(
        "items.html", {"request": request, "todo_list": todo_items}
    )


@app.get("/items/", response_model=list[schemas.TodoItem])
def read_todoitems(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_todoitems(db=db, skip=skip, limit=limit)


@app.put("/items/{item_id}/", response_model=schemas.TodoItem)
def update_todoitem(
    item_id: int, item: schemas.TodoItemUpdate, db: Session = Depends(get_db)
):
    db_item = crud.update_todoitem(db=db, item_id=item_id, item=item)
    if not db_item:
        raise HTTPException(status_code=404, detail="Todo item not found")
    return db_item


@app.delete("/items/{item_id}/", response_model=schemas.TodoItem)
def delete_todoitem(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_todoitem(db=db, item_id=item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Todo item not found")
    return db_item
