from sqlalchemy.orm import Session
from app.auth import models
from app.core.security import hash_password, verify_password, create_access_token

def create_user(db: Session, email: str, password: str ):
    user = models.User(
        email=email,
        hashed_password=hash_password(password)
            )
    db.add(user)
    db.commit()
    print(db.query(models.User))
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def login_user(user):
    return create_access_token({"sub": str(user.id), "role": user.role})
