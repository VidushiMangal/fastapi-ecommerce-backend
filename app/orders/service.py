from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.orders import models
from app.catalog.models import Product
from app.common.enums import OrderStatus

from sqlalchemy import func
from app.orders.models import Order

def create_order(db: Session, user_id: int, items):
    if not items:
        raise HTTPException(status_code=400, detail="Order must contain items")

    order_items = []
    total_amount = 0.0

    for item in items:
        product = db.query(Product).filter( Product.pid == item.product_id, Product.is_active == True).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found" )
        if product.stock < item.quantity:
            raise HTTPException( status_code=400, detail=f"Insufficient stock for product {product.name}")

        price = product.price
        total_amount += price * item.quantity

        order_items.append( models.OrderItem(
                product_id=product.pid,
                quantity=item.quantity,
                price_at_purchase=price
            )
        )
        product.stock -= item.quantity # reduce stock

    order = models.Order(
        user_id=user_id,
        total_amount=total_amount,
        status=OrderStatus.CREATED,
        items=order_items
    )

    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def update_order_status(db: Session, order_id: int, new_status: OrderStatus):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    valid_transitions = {
        OrderStatus.PAID: OrderStatus.SHIPPED,
        OrderStatus.SHIPPED: OrderStatus.COMPLETED
    }

    if order.status not in valid_transitions or valid_transitions[order.status] != new_status:
        raise HTTPException( status_code=400, detail="Invalid order status transition" )
    order.status = new_status
    db.commit()
    db.refresh(order)
    return order

def get_total_orders(db):
    return db.query(func.count(Order.id)).scalar()

def get_total_revenue(db):
    return (
        db.query(func.sum(Order.total_amount))
        .filter(Order.status.in_([
            OrderStatus.PAID,
            OrderStatus.COMPLETED
        ])).scalar()
        or 0.0
    )

def get_orders_by_status(db):
    results = (
        db.query(Order.status, func.count(Order.id))
        .group_by(Order.status)
        .all()
    )
    return {status.value: count for status, count in results}
