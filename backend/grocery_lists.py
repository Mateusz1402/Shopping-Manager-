from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from tables.tables_definition import Memory
from schemas import ListSchema

router = APIRouter(
    prefix="/grocery_lists",
    tags=["Grocery_lists"]
)


@router.get("{index}")
def get_grocery_list(index: int, db: Session = Depends(get_db)):
    list = db.query(Memory).filter(Memory.grocery_list_index == index).all()
    if not list:
        raise HTTPException(status_code=404, detail="Grocery list not found")
    
    return [{
        "product" : l.product,
        "category" : l.category,
        "user" : l.user,
        "index" : l.grocery_list_index,
        "date" : l.created_at
    }
    for l in list
    ]


@router.post("{index}")
def post_grocery_list(schema: ListSchema, db: Session = Depends(get_db)):
    # TO DO

    """
     GOAL:  save the list of ListSchemas into table.
            Add new column: is_active into memory.
    """
    print(1)
