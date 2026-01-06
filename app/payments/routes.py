from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.payments import schemas, service
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.auth.models import User

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/")
def make_payment(
    data: schemas.PaymentRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return service.process_payment(
        db=db,
        order_id=data.order_id,
        success=data.success
    )
