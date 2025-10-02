from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/vehicles",
    tags=["vehicles"],
)

@router.post("/", response_model=schemas.Vehicle)
def create_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    # Añadir validación para asegurar que el owner_id (Client) exista
    return crud.create_vehicle(db=db, vehicle=vehicle)

@router.get("/by_client/{client_id}", response_model=List[schemas.Vehicle])
def read_vehicles_for_client(client_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    vehicles = crud.get_vehicles_by_client(db, client_id=client_id, skip=skip, limit=limit)
    return vehicles
