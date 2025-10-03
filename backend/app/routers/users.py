from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..crud import crud_users
from .. import models, schemas
from ..database import get_db
from ..security import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_user)]
)

@router.get("/", response_model=List[schemas.User])
def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """
    Devuelve una lista de usuarios para el tenant del usuario autenticado.
    """
    users = crud_users.get_users(db, tenant_id=current_user.tenant_id, skip=skip, limit=limit)
    return users

@router.post("/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """
    Crea un nuevo usuario dentro del mismo tenant que el usuario que realiza la acción.
    La pertenencia al tenant se hereda, no se especifica en el body.
    """
    db_user = crud_users.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Aquí asignamos el tenant_id del usuario actual al nuevo usuario.
    user_data = schemas.UserCreateWithTenant(
        **user.dict(), 
        tenant_id=current_user.tenant_id
    )
    return crud_users.create_user(db=db, user=user_data)
