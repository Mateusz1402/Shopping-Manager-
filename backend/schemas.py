from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    category_id: int


class CategoryCreate(BaseModel):
    category_name: str