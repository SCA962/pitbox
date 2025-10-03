from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..crud import crud_clients
from .. import models, schemas
from ..database import get_db
from ..security import get_current_user

router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=schemas.Client)
def create_client(
    client: schemas.ClientCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """
    Crea un nuevo cliente dentro del tenant del usuario autenticado.
    El tenant_id se infiere del token del usuario, no se pasa en el body.
    """
    return crud_clients.create_client(db=db, client=client, tenant_id=current_user.tenant_id)

@router.get("/", response_model=List[schemas.Client])
def read_clients(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Devuelve una lista de todos los clientes del tenant del usuario autenticado.
    """
    clients = crud_clients.get_clients(db, tenant_id=current_user.tenant_id, skip=skip, limit=limit)
    return clients

@router.get("/{client_id}", response_model=schemas.Client)
def read_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Obtiene un cliente específico, verificando que pertenezca al tenant del usuario.
    """
    db_client = crud_clients.get_client(db, client_id=client_id, tenant_id=current_user.tenant_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_client
