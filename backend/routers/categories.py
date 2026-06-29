from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from tables.tables_definition import Categories

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

@router.get("")
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Categories).all()
    return [
        {
            "id" : category.id,
            "category_name" : category.category_name
        }
        for category in categories
    ]