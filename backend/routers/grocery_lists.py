import datetime
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