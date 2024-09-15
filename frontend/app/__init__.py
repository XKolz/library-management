from fastapi import FastAPI
# from .routers import users, books
from .routers import users, books


app = FastAPI()

# app.include_router(books.router, prefix="/admin")
# Register routers
app.include_router(users.router)
app.include_router(books.router)
