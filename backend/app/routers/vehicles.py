from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..crud import crud_vehicles, crud_clients
from .. import models, schemas
from ..database import get_db
from ..security import get_current_user

router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=schemas.Vehicle)
def create_vehicle(
    vehicle: schemas.VehicleCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """
    Crea un nuevo vehículo, asegurando que el propietario (cliente) exista en el tenant.
    """
    # Verificación de seguridad: El cliente (owner) debe existir en el tenant del usuario.
    db_client = crud_clients.get_client(db, client_id=vehicle.owner_id, tenant_id=current_user.tenant_id)
    if not db_client:
        raise HTTPException(
            status_code=404, 
            detail=f"Cliente con id {vehicle.owner_id} no encontrado en tu tenant."
        )
    return crud_vehicles.create_vehicle(db=db, vehicle=vehicle)

@router.get("/", response_model=List[schemas.Vehicle])
def read_vehicles(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Devuelve una lista de todos los vehículos del tenant del usuario.
    """
    vehicles = crud_vehicles.get_vehicles(db, tenant_id=current_user.tenant_id, skip=skip, limit=limit)
    return vehicles

@router.get("/{vehicle_id}", response_model=schemas.Vehicle)
def read_vehicle(
    vehicle_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Obtiene un vehículo específico, verificando que pertenezca al tenant.
    """
    db_vehicle = crud_vehicles.get_vehicle(db, vehicle_id=vehicle_id, tenant_id=current_user.tenant_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return db_vehicle
