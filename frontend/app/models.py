from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    publisher = Column(String)
    category = Column(String)
    available = Column(Boolean, default=True)
    borrower_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    borrowed_until = Column(DateTime, nullable=True)

    borrower = relationship("User")
