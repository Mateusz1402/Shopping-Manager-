import datetime
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import func, distinct
from sqlalchemy.orm import Session
from database import get_db
from tables.tables_definition import Memory, Categories
from schemas import ListSchema

router = APIRouter(
    prefix="/grocery_lists",
    tags=["Grocery_lists"]
)

# GET entire grocery list
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

# POST to save new grocery list
@router.post("/{index}")
def post_grocery_list(index: int, schema: list[ListSchema], db: Session = Depends(get_db)):
    if len(schema) < 1:
        raise HTTPException(status_code=404, detail="Grocery list is empty")
    is_index_used = bool(db.query(Memory).filter(Memory.grocery_list_index == index).first())
    if is_index_used:
        raise HTTPException(status_code=404, detail="The index is already used")
    if index <= 0:
        raise HTTPException(status_code=404, detail="Wrong index value")
    
    date = datetime.datetime.now()
    for i in range(len(schema)):
        grocery_item = Memory(product=schema[i].product,
                              category=schema[i].category,
                              user=schema[i].user,
                              grocery_list_index=index,
                              active=True,
                              created_at=date
                              )
        db.add(grocery_item)
    db.commit()
    db.refresh(grocery_item)
    return {
        "message" : "Grocery list saved successfully"
    }

# PATCH unactive existing grocery list
@router.patch("/unactive/{index}")
def patch_unactive_grocery_list(index: int, db: Session = Depends(get_db)):
    index_exists = bool(db.query(Memory).filter(Memory.grocery_list_index == index).first())
    if not index_exists:
        raise HTTPException(status_code=404, detail="Incorrect index")
    grocery_list = db.query(Memory).filter(Memory.grocery_list_index == index).all()

    for g in grocery_list:
        g.active = False
    db.commit()
    return{
        "message" : "Grocery list unactive successfully"
    }


# GET amount of active grocery lists
@router.get("/actives")
def get_amount_of_active_lists(db: Session = Depends(get_db)):
    amount = db.query(func.count(distinct(Memory.grocery_list_index))).filter(Memory.active == True).scalar()
    return amount

# GET latest active grocery list
@router.get("/latest_active")
def get_latest_active_grocery_list(db: Session = Depends(get_db)):
    highest_index = db.query(func.max(Memory.grocery_list_index)).filter(Memory.active == True).scalar()
    latest = db.query(Memory)\
        .join(Categories, Memory.category == Categories.category_name)\
        .filter(Memory.active == True, Memory.grocery_list_index == highest_index)\
        .order_by(Categories.id.asc())\
        .all()
    if not latest:
        raise HTTPException(status_code=404, detail="No latest active grocery list in db")
    return [
        {
            "product" : l.product,
            "category" : l.category
        } for l in latest
    ]