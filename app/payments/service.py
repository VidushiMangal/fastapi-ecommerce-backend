from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.orders.models import Order
from app.common.enums import OrderStatus


def process_payment(db: Session, order_id: int, success: bool):
    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != OrderStatus.CREATED:
        raise HTTPException(
            status_code=400,
            detail="Payment not allowed for this order state"
        )

    if success:
        order.status = OrderStatus.PAID
    else:
        order.status = OrderStatus.FAILED

    db.commit()
    db.refresh(order)
    return order
