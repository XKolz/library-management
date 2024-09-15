import requests
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import BookAdmin, BorrowedBook
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# URL of the frontend API
FRONTEND_API_URL = "http://frontend_api:8000/books/sync/"

class BookCreate(BaseModel):
    title: str
    author: str
    publisher: str
    category: str

class BorrowedBookSync(BaseModel):
    book_id: int
    title: str
    author: str
    borrower_name: str
    borrowed_until: str

@router.post("/admin/books/")
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    # Add the book to the backend database
    new_book = BookAdmin(
        title=book.title,
        author=book.author,
        publisher=book.publisher,
        category=book.category
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    # Notify the frontend API to sync the book
    sync_data = {
        "title": new_book.title,
        "author": new_book.author,
        "publisher": new_book.publisher,
        "category": new_book.category
    }
    try:
        response = requests.post(FRONTEND_API_URL, json=sync_data)
        if response.status_code != 200:
            raise Exception("Failed to sync with frontend")
    except Exception as e:
        print(f"Error syncing book: {e}")
    
    return {"message": "Book added and synced with frontend", "book": new_book}


@router.delete("/admin/books/{book_id}")
def remove_book(book_id: int, db: Session = Depends(get_db)):
    # Check if the book exists
    book = db.query(BookAdmin).filter(BookAdmin.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Delete the book from the database
    db.delete(book)
    db.commit()

    return {"message": f"Book with ID {book_id} has been removed"}


# # Sync borrowed books from frontend
# @router.post("/admin/books/borrowed/")
# def sync_borrowed_book(borrowed_data: BorrowedBookSync, db: Session = Depends(get_db)):
#     # Check if the book already exists in the backend database
#     existing_book = db.query(BookAdmin).filter(BookAdmin.id == borrowed_data.book_id).first()
#     if not existing_book:
#         raise HTTPException(status_code=404, detail="Book not found in backend database")
    
#     # Sync borrowed book record
#     borrowed_book = BorrowedBook(
#         book_id=borrowed_data.book_id,
#         borrower_name=borrowed_data.borrower_name,
#         borrowed_until=datetime.fromisoformat(borrowed_data.borrowed_until)
#     )
#     db.add(borrowed_book)
#     db.commit()
#     db.refresh(borrowed_book)

#     return {"message": "Borrowed book synced with backend", "borrowed_book": borrowed_book}

@router.post("/admin/books/borrowed/")
def sync_borrowed_book(borrowed_data: BorrowedBookSync, db: Session = Depends(get_db)):
    # Check if the book already exists in the backend database
    existing_book = db.query(BookAdmin).filter(BookAdmin.id == borrowed_data.book_id).first()
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found in backend database")
    
    # Mark the book as unavailable in the backend
    existing_book.available = False
    
    # Sync the borrowed book record
    borrowed_book = BorrowedBook(
        book_id=borrowed_data.book_id,
        borrower_name=borrowed_data.borrower_name,
        borrowed_until=datetime.fromisoformat(borrowed_data.borrowed_until)
    )
    db.add(borrowed_book)
    db.commit()
    db.refresh(borrowed_book)

    return {"message": "Borrowed book synced with backend", "borrowed_book": borrowed_book}



# Get all borrowed books with borrower details
@router.get("/admin/books/borrowed/")
def list_borrowed_books(db: Session = Depends(get_db)):
    borrowed_books = db.query(BorrowedBook).all()
    if not borrowed_books:
        raise HTTPException(status_code=404, detail="No borrowed books found")
    
    return borrowed_books

@router.get("/admin/books/unavailable/")
def list_unavailable_books(db: Session = Depends(get_db)):
    # Query to find all borrowed books (those that are unavailable)
    borrowed_books = db.query(BorrowedBook).all()
    
    if not borrowed_books:
        raise HTTPException(status_code=404, detail="No unavailable books found")
    
    return borrowed_books

# Sync borrowed books from frontend to backend
@router.post("/admin/books/borrowed/")
def sync_borrowed_book(borrowed_data: BorrowedBookSync, db: Session = Depends(get_db)):
    # Check if the book already exists in the backend database
    existing_book = db.query(BookAdmin).filter(BookAdmin.id == borrowed_data.book_id).first()
    if not existing_book:
        raise HTTPException(status_code=404, detail="Book not found in backend database")
    
    # Sync borrowed book record
    borrowed_book = BorrowedBook(
        book_id=borrowed_data.book_id,
        borrower_name=borrowed_data.borrower_name,
        borrowed_until=datetime.fromisoformat(borrowed_data.borrowed_until)
    )
    db.add(borrowed_book)
    db.commit()
    db.refresh(borrowed_book)

    return {"message": "Borrowed book synced with backend", "borrowed_book": borrowed_book}

# Get all books
@router.get("/admin/books/")
def list_books(category: str = Query(None), publisher: str = Query(None), db: Session = Depends(get_db)):
    query = db.query(BookAdmin)
    
    # Apply filters if provided
    if category:
        query = query.filter(BookAdmin.category == category)
    if publisher:
        query = query.filter(BookAdmin.publisher == publisher)
    
    books = query.all()

    if not books:
        raise HTTPException(status_code=404, detail="No books found with the given filters")
    
    return books

@router.get("/admin/books/{book_id}")
def get_book_by_id(book_id: int, db: Session = Depends(get_db)):
    book = db.query(BookAdmin).filter(BookAdmin.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    return book