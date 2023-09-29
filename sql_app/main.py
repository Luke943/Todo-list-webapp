from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
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
def read_root():
    return RedirectResponse(url="/login/")


@app.get("/login/", response_class=HTMLResponse)
def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login/", response_class=RedirectResponse)
def login_user(username: str = Form(...), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return RedirectResponse(
        url=f"/users/{db_user.id}/items/", status_code=status.HTTP_302_FOUND
    )


@app.get("/register/", response_class=HTMLResponse)
def read_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


"""
Users
"""


# @app.post("/users/", response_model=schemas.User)
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_username(db=db, username=user.username)
#     if db_user:
#         raise HTTPException(status_code=400, detail="Username already exists")
#     return crud.create_user(db=db, user=user)


# @app.get("/users/", response_model=list[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return crud.get_users(db=db, skip=skip, limit=limit)


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db=db, user_id=user_id)
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.put("/users/{user_id}", response_model=schemas.User)
# def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
#     db_user = crud.update_user(db=db, user_id=user_id, user=user)
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.delete("/users/{user_id}", response_model=schemas.User)
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.delete_user(db=db, user_id=user_id)
#     if not db_user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


"""
Todo Items
"""


@app.get("/users/{user_id}/items/", response_class=HTMLResponse)
def read_todoitems_for_user(
    request: Request,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    todo_items = crud.get_user_todoitems(db, user_id, skip, limit)
    return templates.TemplateResponse(
        "items.html", {"request": request, "todo_list": todo_items}
    )


@app.post("/users/{user_id}/items/", response_class=RedirectResponse)
def create_todoitem_for_user(
    user_id: int, title: str = Form(...), db: Session = Depends(get_db)
):
    item = schemas.TodoItemCreate(text=title)
    crud.create_user_todoitem(db, item, user_id)
    return RedirectResponse(
        url=f"/users/{user_id}/items/", status_code=status.HTTP_302_FOUND
    )


# @app.get("/items/", response_model=list[schemas.TodoItem])
# def read_todoitems(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     return crud.get_todoitems(db=db, skip=skip, limit=limit)


@app.post("/items/{item_id}/")
def todoitem_request_handler(item_id: int, method: str = Form(...)):
    if method == "_delete":
        return RedirectResponse(url=f"/items/{item_id}/delete/")
    if method == "_update":
        return RedirectResponse(url=f"/items/{item_id}/update/")
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Method not found"
    )


@app.post("/items/{item_id}/update/", response_class=RedirectResponse)
def update_todoitem(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.update_status_todoitem(db, item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found"
        )
    user_id = db_item.owner_id
    return RedirectResponse(
        url=f"/users/{user_id}/items/", status_code=status.HTTP_302_FOUND
    )


@app.post("/items/{item_id}/delete/", response_class=RedirectResponse)
def delete_todoitem(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_todoitem(db, item_id)
    if not db_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo item not found"
        )
    user_id = db_item.owner_id
    return RedirectResponse(
        url=f"/users/{user_id}/items/", status_code=status.HTTP_302_FOUND
    )
