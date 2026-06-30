from fastapi import FastAPI, Depends, HTTPException
from database import get_db
from routers import products, categories, auth
from tables.tables_definition import Products, Categories
from schemas import ProductCreate
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Grocery Shopping API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
app.include_router(products.router)
app.include_router(categories.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Grocery Shpping API"}