from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas
from ..database import get_db
from ..security import get_current_user

router = APIRouter(
    prefix="/clients",
    tags=["Clients"], # Consistencia en mayúsculas
    # ¡Este es el interruptor maestro! Todas las rutas en este router
    # ahora requerirán autenticación sin tener que especificarlo en cada una.
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=schemas.Client)
def create_client(
    client: schemas.ClientCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """
    Crea un nuevo cliente para el tenant del usuario autenticado.
    - El `tenant_id` se extrae de forma segura del token del usuario.
    - Ya no es posible crear un cliente en un tenant ajeno.
    """
    # Pasamos el tenant_id del usuario actual a la función del CRUD
    return crud.create_client(db=db, client=client, tenant_id=current_user.tenant_id)

@router.get("/", response_model=List[schemas.Client])
def read_clients(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Devuelve una lista de clientes **solo para el tenant del usuario autenticado**.
    - Previene la fuga de datos entre tenants.
    """
    clients = crud.get_clients(db, tenant_id=current_user.tenant_id, skip=skip, limit=limit)
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
    db_client = crud.get_client(db, client_id=client_id, tenant_id=current_user.tenant_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return db_client
