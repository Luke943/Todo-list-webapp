from fastapi import Depends, FastAPI, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
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


"""
Login
"""


@app.get("/login/", response_class=HTMLResponse)
def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login/", response_class=RedirectResponse)
def login_user(username: str = Form(...), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username)
    if not db_user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return RedirectResponse(f"/users/{db_user.id}/items/", status.HTTP_302_FOUND)


"""
Register
"""


@app.get("/register/", response_class=HTMLResponse)
def read_register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.post("/register/", response_class=RedirectResponse)
def create_user(username: str = Form(...), db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username)
    if db_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Username already exists")
    user = schemas.UserCreate(username=username)
    db_user = crud.create_user(db, user)
    return RedirectResponse(f"/users/{db_user.id}/items/", status.HTTP_302_FOUND)


"""
Todo Items
"""


@app.get("/users/{user_id}/items/", response_class=HTMLResponse)
def read_todoitems_for_user(
    request: Request,
    user_id: int,
    filter: bool = False,
    db: Session = Depends(get_db),
):
    user = crud.get_user(db, user_id)
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    todo_items = crud.get_user_todoitems(db, user_id)
    return templates.TemplateResponse(
        "items.html",
        {
            "request": request,
            "username": user.username,
            "todo_list": todo_items,
            "filter": filter,
        },
    )


@app.post("/users/{user_id}/items/", response_class=RedirectResponse)
def create_todoitem_for_user(
    user_id: int, title: str = Form(...), db: Session = Depends(get_db)
):
    item = schemas.TodoItemCreate(text=title)
    crud.create_user_todoitem(db, item, user_id)
    return RedirectResponse(f"/users/{user_id}/items/", status.HTTP_302_FOUND)


@app.post("/items/{item_id}/")
def todoitem_request_handler(item_id: int, method: str = Form(...)):
    if method == "_delete":
        return RedirectResponse(f"/items/{item_id}/delete/")
    if method == "_update":
        return RedirectResponse(f"/items/{item_id}/update/")
    raise HTTPException(status.HTTP_400_BAD_REQUEST, "Method not found")


@app.post("/items/{item_id}/update/", response_class=RedirectResponse)
def update_todoitem(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.update_status_todoitem(db, item_id)
    if not db_item:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Todo item not found")
    user_id = db_item.owner_id
    return RedirectResponse(f"/users/{user_id}/items/", status.HTTP_302_FOUND)


@app.post("/items/{item_id}/delete/", response_class=RedirectResponse)
def delete_todoitem(item_id: int, db: Session = Depends(get_db)):
    db_item = crud.delete_todoitem(db, item_id)
    if not db_item:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Todo item not found")
    user_id = db_item.owner_id
    return RedirectResponse(f"/users/{user_id}/items/", status.HTTP_302_FOUND)
