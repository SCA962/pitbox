from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/clients",
    tags=["clients"],
)

@router.post("/", response_model=schemas.Client)
def create_client(client: schemas.ClientCreate, db: Session = Depends(get_db)):
    # Añadir validación para asegurar que el tenant exista
    return crud.create_client(db=db, client=client)

@router.get("/{tenant_id}", response_model=List[schemas.Client])
def read_clients_for_tenant(tenant_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    clients = crud.get_clients(db, tenant_id=tenant_id, skip=skip, limit=limit)
    return clients
