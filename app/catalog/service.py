from sqlalchemy.orm import Session
from app.catalog import models

def create_category(db: Session, name: str):
    category = models.Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

def create_product(db: Session, data):
    product = models.Product(**data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

def list_products(db: Session):
    return db.query(models.Product).filter(models.Product.is_active == True).all()
