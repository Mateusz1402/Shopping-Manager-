from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, distinct
from sqlalchemy.orm import Session
from database import get_db
from tables.tables_definition import Products, Categories
from schemas import ProductCreate


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


# GET all of defined products according to their categories
@router.get("")
def get_products(db: Session = Depends(get_db)):
    results = db.query(Products, Categories.category_name)\
                .join(Categories, Categories.id == Products.category_id)\
                .order_by(Products.id.asc())\
                .all()
    return [
        {
            "product" : product.name,
            "category" : category,
            "id" : product.id,
            "active_product" : product.is_ordered
            #"grocery_list_index" : 1
        }
        for product, category in results
    ]


@router.patch("/{product_id}/toggle")
def toggle_product_status(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Products).filter(Products.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.is_ordered = not product.is_ordered
    db.commit()
    db.refresh(product)
    return {
        "message" : f"Updated the status of {product.name}", 
        "is_ordered" : product.is_ordered
    }


@router.post("")
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    existing_product = db.query(Products).filter(
        Products.name.ilike(product_data.name.strip())
    ).first()

    if existing_product:
        raise HTTPException(
            status_code=400,
            detail=f"Product '{product_data.name}' already exists!"
        )
    
    new_product = Products(
        name = product_data.name.strip(),
        category_id = product_data.category_id,
        is_ordered = False
    ) 
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {
        "message" : "Product created successfully",
        "product" : {"id" : new_product.id,
                     "name" : new_product.name}
    }


@router.delete("/{product_name}")
def delete_product(product_name: str, db: Session = Depends(get_db)):
    existing_product = db.query(Products).filter(Products.name == product_name).first()

    if not existing_product:
        raise HTTPException(status_code=400, detail="Product not found")
    
    db.delete(existing_product)
    db.commit()
    return {
        "message" : f"The product {existing_product.name} successfully deleted."
    }
    