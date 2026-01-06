from pydantic import BaseModel
from typing import Optional

class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(BaseModel):
    category_id: int
    name: str
    class Config: # this is pydantic configuration mechanism. it convers ORM object in to dictionary.
        from_attributes = True

class ProductCreate(BaseModel):
    name: str
    description: Optional[str]
    price: float
    stock: int
    category_id: int

class ProductResponse(BaseModel):
    pid: int
    name: str
    price: float
    stock: int
    category: CategoryResponse
    class Config:
        from_attributes = True


