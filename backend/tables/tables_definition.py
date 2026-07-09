from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Float
from sqlalchemy.sql import func

string_db = "postgresql://postgres:postgres@localhost:5432/grocery_shopping_db"
engine = create_engine(string_db)
Base = declarative_base()


# categories table
class Categories(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    category_name = Column(String, nullable=False, unique=True)


# products table
class Products(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    is_ordered = Column(Boolean, nullable=False, default=False)


# users table
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False, default="guest")


# memory table
class Memory(Base):
    __tablename__ = 'memory'
    id = Column(Integer, primary_key=True)
    product = Column(String, ForeignKey('products.name'), nullable=False)
    category = Column(String, ForeignKey('categories.category_name'), nullable=False)
    user = Column(String, ForeignKey('users.username'), nullable=False)
    grocery_list_index = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

Base.metadata.create_all(engine)




