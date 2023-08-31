from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(index=True)
    # hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)

    items = relationship("TodoItem", back_populates="owner")

    def __repr__(self) -> str:
        return (
            f"User(id={self.id}, username={self.username}, is_active={self.is_active})"
        )


class TodoItem(Base):
    __tablename__ = "todo_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(50))
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")

    def __repr__(self) -> str:
        return f"TodoItem(id={self.id}, text={self.text}, done={self.done})"
