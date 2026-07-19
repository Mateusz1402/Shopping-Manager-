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
                              active_list=True,
                              active_product=True,
                              created_at=date
                              )
        db.add(grocery_item)
    db.commit()
    db.refresh(grocery_item)
    return {
        "message" : "Grocery list saved successfully"
    }


# GET amount of active grocery lists
@router.get("/actives")
def get_amount_of_active_lists(db: Session = Depends(get_db)):
    amount = db.query(func.count(distinct(Memory.grocery_list_index))).filter(Memory.active_list == True).scalar()
    return amount


# GET latest active grocery list
@router.get("/latest_active")
def get_latest_active_grocery_list(db: Session = Depends(get_db)):
    highest_active_index = db.query(func.max(Memory.grocery_list_index)).filter(Memory.active_list == True).scalar()
    latest = db.query(Memory)\
        .join(Categories, Memory.category == Categories.category_name)\
        .filter(Memory.active_list == True, Memory.grocery_list_index == highest_active_index)\
        .order_by(Categories.id.desc())\
        .all()
    if not latest:
        raise HTTPException(status_code=404, detail="No active lists!")

    return [
        {   
            "product" : l.product,
            "category" : l.category,
            "id" : l.id,
            "active_product" : l.active_product,
            "grocery_list_index" : l.grocery_list_index
        } for l in latest
    ]


# GET metadata of active grocery lists
@router.get("/metadata")
def get_metadata(db: Session = Depends(get_db)):
    highest_index = db.query(func.max(Memory.grocery_list_index)).scalar()
    if not highest_index or highest_index == 0:
        raise HTTPException(status_code=404, details="Wrong max. grocery index!")
    total_active_lists = 0
    for i in range(1, highest_index):
        is_active = db.query(Memory).filter(Memory.grocery_list_index == i, Memory.active_list == True).first() is not None
        if is_active:
            total_active_lists += 1
    last_created_at = db.query(Memory).filter(Memory.grocery_list_index == highest_index).first()
    return {
        "total_lists" : highest_index,
        "total_active_lists" : total_active_lists,
        "last_created_at" : last_created_at.created_at.strftime("%Y-%m-%d  %H:%M:%S")
    }


# PATCH for toggling the active status of the product
@router.patch("/toggle/{index}")
def patch_toggle_active_status(index: int, db: Session = Depends(get_db)):
    if index < 0:
        raise HTTPException(status_code=404, detail="Prohibit product index!")
    obj = db.query(Memory).filter(Memory.id == index).first()
    if not obj:
        raise HTTPException(status_code=404, detail="No searching product")
    obj.active_product = not obj.active_product
    db.commit()
    db.refresh(obj)
    return {
        "message" : "Toggling active status of the product finish with success",
        "actual_state" : obj.active_product
    }


# PATCH unactive grocery list with all bought products
@router.patch("/inactive/{index}")
def patch_unactive_grocery_list(index: int, db: Session = Depends(get_db)):
    index_exists = bool(db.query(Memory).filter(Memory.grocery_list_index == index).first())
    if not index_exists:
        raise HTTPException(status_code=404, detail="Incorrect index")
    grocery_list = db.query(Memory).filter(Memory.grocery_list_index == index).all()

    list_is_empty = True
    for g in grocery_list:
        if g.active_product != False:
            list_is_empty = False
    if list_is_empty:
        for g in grocery_list:
            g.active_list = False
        db.commit()
    else:
        raise HTTPException(status_code=404, detail="Can not disactive list due to active products!")
    return{
        "message" : "Grocery list unactive successfully"
    }