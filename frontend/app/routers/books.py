import requests
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from ..database import get_db
from pydantic import BaseModel
from ..models import Book, User
from datetime import datetime, timedelta

router = APIRouter()

# URL of the backend API
BACKEND_API_URL = "http://backend_api:8001/admin/books/"

# Pydantic model for syncing books
class SyncBook(BaseModel):
    title: str
    author: str
    publisher: str
    category: str

# Get all books
@router.get("/books/")
def get_books(category: str = Query(None), publisher: str = Query(None)):
    try:
        # Prepare the query parameters
        params = {}
        if category:
            params["category"] = category
        if publisher:
            params["publisher"] = publisher

        # Fetch books from the Backend API with optional filtering
        response = requests.get(BACKEND_API_URL, params=params)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch books from backend")
        
        books = response.json()
        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching books from backend: {e}")

# Get a single book by ID
# @router.get("/books/{id}")
# def get_book_by_id(id: int, db: Session = Depends(get_db)):
#     book = db.query(Book).filter(Book.id == id).first()
#     if not book:
#         raise HTTPException(status_code=404, detail="Book not found")
#     return book

@router.get("/books/{book_id}")
def get_book_by_id(book_id: int):
    try:
        # Fetch the book by ID from the Backend API
        response = requests.get(f"{BACKEND_API_URL}{book_id}")
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail="Book not found")
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch book from backend")
        
        book = response.json()
        return book
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching book from backend: {e}")

# @router.post("/books/borrow/{id}")
# def borrow_book(id: int, days: int, user_id: int, db: Session = Depends(get_db)):
#     # Check if the book is available
#     book = db.query(Book).filter(Book.id == id, Book.available == True).first()
#     if not book:
#         raise HTTPException(status_code=404, detail="Book is not available for borrowing")
    
#     # Find the user who is borrowing the book
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")

#     # Mark the book as borrowed
#     book.available = False
#     book.borrower_id = user.id
#     book.borrowed_until = datetime.utcnow() + timedelta(days=days)
    
#     db.commit()
#     db.refresh(book)

#     # Notify the backend about the borrowed book
#     backend_url = "http://backend_api:8001/admin/books/borrowed/"
#     try:
#         borrowed_data = {
#             "book_id": book.id,
#             "title": book.title,
#             "author": book.author,
#             "borrower_name": f"{user.first_name} {user.last_name}",
#             "borrowed_until": book.borrowed_until.isoformat(),
#         }
#         # Send the book data to the backend
#         response = requests.post(backend_url, json=borrowed_data)
#         if response.status_code != 200:
#             raise HTTPException(status_code=response.status_code, detail="Failed to notify backend about borrowed book")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error notifying backend: {e}")

#     return {"message": f"Book borrowed for {days} days by {user.first_name} {user.last_name}", "book": book}

@router.post("/books/borrow/{id}")
def borrow_book(id: int, days: int, user_id: int, db: Session = Depends(get_db)):
    # Fetch the book details from the backend (to make sure it's available)
    backend_book_url = f"http://backend_api:8001/admin/books/{id}"
    book_response = requests.get(backend_book_url)
    
    if book_response.status_code == 404:
        raise HTTPException(status_code=404, detail="Book not found in backend")
    
    backend_book = book_response.json()
    
    # Check if the book is available
    if not backend_book.get("available", True):
        raise HTTPException(status_code=404, detail="Book is not available for borrowing")
    
    # Find the user who is borrowing the book
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Mark the book as borrowed in the frontend
    new_borrowed_book = Book(
        id=backend_book['id'],
        title=backend_book['title'],
        author=backend_book['author'],
        publisher=backend_book['publisher'],
        category=backend_book['category'],
        available=False,
        borrower_id=user.id,
        borrowed_until=datetime.utcnow() + timedelta(days=days),
    )
    db.add(new_borrowed_book)
    db.commit()

    # Notify the backend about the borrowed book
    backend_borrow_url = "http://backend_api:8001/admin/books/borrowed/"
    try:
        borrowed_data = {
            "book_id": backend_book['id'],
            "title": backend_book['title'],
            "author": backend_book['author'],
            "borrower_name": f"{user.first_name} {user.last_name}",
            "borrowed_until": new_borrowed_book.borrowed_until.isoformat(),
        }
        response = requests.post(backend_borrow_url, json=borrowed_data)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to notify backend about borrowed book")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error notifying backend: {e}")

    return {"message": f"Book borrowed for {days} days by {user.first_name} {user.last_name}", "book": new_borrowed_book}
