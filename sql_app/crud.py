from sqlalchemy.orm import Session

from . import models, schemas

# Users


def create_user(db: Session, user: schemas.UserCreate):
    # hash password would go here
    db_user = models.User(username=user.username)
    db.add(db_user)
    db.commit()
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        user_data = user.model_dump(exclude_unset=True)
        for key, value in user_data.items():
            setattr(db_user, key, value)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user


# Todo Items


def create_user_todoitem(db: Session, item: schemas.TodoItemCreate, user_id: int):
    db_item = models.TodoItem(**item.model_dump(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_todoitems(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TodoItem).offset(skip).limit(limit).all()


def update_todoitem(db: Session, item_id: int, item: schemas.TodoItemUpdate):
    db_item = db.query(models.TodoItem).filter(models.TodoItem.id == item_id).first()
    if db_item:
        item_data = item.dict(exclude_unset=True)
        for key, value in item_data.items():
            setattr(db_item, key, value)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
    return db_item


def delete_todoitem(db: Session, item_id: int):
    db_item = db.query(models.TodoItem).filter(models.TodoItem.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
    return db_item
