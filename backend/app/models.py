
# from sqlalchemy import Column, Integer, String, Boolean
# from .database import Base

# class BookAdmin(Base):
#     __tablename__ = "books"
#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String)
#     author = Column(String)
#     publisher = Column(String)
#     category = Column(String)
#     available = Column(Boolean, default=True)

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .database import Base

class BookAdmin(Base):
    __tablename__ = 'books_admin'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String)
    publisher = Column(String)
    category = Column(String)
    available = Column(Boolean, default=True)

class BorrowedBook(Base):
    __tablename__ = 'borrowed_books'

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer)
    borrower_name = Column(String)
    borrowed_until = Column(DateTime)


# class BorrowedBook(Base):
#     __tablename__ = 'borrowed_books'

#     id = Column(Integer, primary_key=True, index=True)
#     book_id = Column(Integer, index=True)
#     borrower_name = Column(String)
#     borrowed_until = Column(DateTime)