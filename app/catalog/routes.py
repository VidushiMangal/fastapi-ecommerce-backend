from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.catalog import schemas, service
from app.core.database import get_db
from app.core.dependencies import admin_only

router = APIRouter(prefix="/catalog", tags=["Catalog"])

@router.post("/categories", dependencies=[Depends(admin_only)]) 
def create_category(data: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return service.create_category(db, data.name)

@router.post("/products", dependencies=[Depends(admin_only)])
def create_product(data: schemas.ProductCreate, db: Session = Depends(get_db)):
    return service.create_product(db, data)

@router.get("/products", response_model=list[schemas.ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return service.list_products(db)
