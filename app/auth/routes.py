from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth import schemas, service
from app.auth.models import User,UserRole
from app.core.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return service.create_user(db, user.email, user.password)

@router.post("/login", response_model=schemas.Token)
def login(data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = service.authenticate_user(db, data.email, data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = service.login_user(user)
    return {"access_token": token}

@router.get("/users_all",response_model=list[schemas.UserResponse])
def get_users(db:Session=Depends(get_db)):
    return db.query(User).filter(User.role == UserRole.CUSTOMER).all()

