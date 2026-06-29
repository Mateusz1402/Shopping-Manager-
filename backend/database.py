from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine


DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/grocery_shopping_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()