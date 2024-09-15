from fastapi import FastAPI
from app.database import init_db
from app import models
# from app.routers import users
from app.routers import users, books

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Library Management System (Frontend)!"}


app.include_router(users.router)
app.include_router(books.router)