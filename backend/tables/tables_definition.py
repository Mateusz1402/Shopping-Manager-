from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean, Float

string_db = "postgresql://postgres:postgres@localhost:5432/grocery_shopping_db"
engine = create_engine(string_db)
Base = declarative_base()

#categories table
class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    category_name = Column(String, nullable=False, unique=True)


#products table
class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    is_ordered = Column(Boolean, nullable=False, default=False)

Base.metadata.create_all(engine)




