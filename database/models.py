from sqlalchemy import Column, Integer, String, DateTime, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.orm import DeclarativeBase, declared_attr, relationship


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class User(Base):
    id_user = Column(Integer, primary_key=True)
    posts = relationship("Task", back_populates="user")


class Task(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id_user"))
    description = Column(String)
    due_date = Column(DateTime)

    user = relationship("User", back_populates="posts")

    __table_args__ = (
        UniqueConstraint('id', 'user_id', name='uix_user_list'),
    )
