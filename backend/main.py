from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from tables.tables_definition import Products, Categories


app = FastAPI(title="Grocery Shopping API")
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/grocery_shopping_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#endspoints
@app.get("/")
def root():
    return {"message": "Welcome to the Grocery Shpping API"}

@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Products).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "category_id": p.category_id,
            "is_ordered": p.is_ordered
        }
        for p in products
    ]

@app.patch("/products/{product_id}/toggle")
def toggle_product_status(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Products).filter(Products.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product.is_ordered = not product.is_ordered
    db.commit()
    db.refresh(product)
    return {"message": f"Updated the status of {product.name}", "is_ordered": product.is_ordered}