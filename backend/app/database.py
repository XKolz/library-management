from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./backend.db"  # For frontend
# Alternatively, "sqlite:///./backend.db" for backend

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get a new database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to initialize the database (creating tables, etc.)
def init_db():
    Base.metadata.create_all(bind=engine)
