from sqlalchemy.orm import Session

from .. import models, schemas
from ..security import get_password_hash

# --- User --- 

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, tenant_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.User).filter(models.User.tenant_id == tenant_id).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password, tenant_id=user.tenant_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
