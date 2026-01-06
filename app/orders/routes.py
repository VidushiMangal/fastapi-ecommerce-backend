from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.orders import schemas, service
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.auth.models import User
from app.common.enums import OrderStatus

from app.core.dependencies import admin_only
from fastapi import Query


router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=schemas.OrderOut)
def place_order(
    data: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.create_order(
        db=db,
        user_id=current_user.id,
        items=data.items
    )

@router.patch("/{order_id}/status",dependencies=[Depends(admin_only)])
def change_order_status(order_id: int,status: OrderStatus = Query(...),db: Session = Depends(get_db),):
        return service.update_order_status(db, order_id, status)

@router.get("/analytics/total-orders",dependencies=[Depends(admin_only)])
def total_orders(db: Session = Depends(get_db)):
    return {
        "total_orders": service.get_total_orders(db)
    }

@router.get("/analytics/total-revenue",dependencies=[Depends(admin_only)])
def total_revenue(db: Session = Depends(get_db)):
    return {
        "total_revenue": service.get_total_revenue(db)
    }

@router.get("/analytics/orders-by-status",dependencies=[Depends(admin_only)])
def orders_by_status(db: Session = Depends(get_db)):
    return service.get_orders_by_status(db)
