from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas
from ..database import get_db
from ..security import get_current_user

router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"], # Consistencia
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=schemas.Vehicle)
def create_vehicle(
    vehicle: schemas.VehicleCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """
    Crea un nuevo vehículo para un cliente, con validación de pertenencia al tenant.
    """
    # **VALIDACIÓN CRÍTICA**: Antes de crear el vehículo, verificamos que el cliente (owner)
    # al que se va a asignar existe DENTRO del tenant del usuario actual.
    owner_client = crud.get_client(db, client_id=vehicle.owner_id, tenant_id=current_user.tenant_id)
    if not owner_client:
        # Si el cliente no existe o no pertenece a este tenant, se rechaza la operación.
        # Esto previene que un taller cree vehículos para clientes de otro taller.
        raise HTTPException(
            status_code=404, 
            detail=f"Cliente con id {vehicle.owner_id} no encontrado en tu tenant."
        )
    
    # Si la validación es exitosa, procedemos a crear el vehículo.
    return crud.create_vehicle(db=db, vehicle=vehicle)

@router.get("/", response_model=List[schemas.Vehicle])
def read_vehicles(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Devuelve una lista de todos los vehículos del tenant del usuario autenticado.
    """
    vehicles = crud.get_vehicles(db, tenant_id=current_user.tenant_id, skip=skip, limit=limit)
    return vehicles

@router.get("/{vehicle_id}", response_model=schemas.Vehicle)
def read_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Obtiene un vehículo específico, verificando que pertenezca al tenant del usuario.
    """
    db_vehicle = crud.get_vehicle(db, vehicle_id=vehicle_id, tenant_id=current_user.tenant_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return db_vehicle
