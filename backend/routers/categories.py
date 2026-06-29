from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from tables.tables_definition import Categories
from schemas import CategoryCreate

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


@router.post("")
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    existing_category = db.query(Categories).filter(
        Categories.category_name.ilike(category.category_name.strip())
    ).first()

    if existing_category:
        raise HTTPException(
            status_code=400,
            detail=f"Category '{category.category_name}' already exists!"
        )

    new_category = Categories(
        category_name = category.category_name.strip()
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return {
        "message" : "Successfully created new category!",
        "category" : {
                        "id" : new_category.id, 
                        "category_name" : new_category.category_name
                    }
    }