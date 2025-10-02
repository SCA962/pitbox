from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..database import get_db

router = APIRouter(
    prefix="/work_orders",
    tags=["work_orders"],
)

@router.post("/", response_model=schemas.WorkOrder)
def create_work_order(work_order: schemas.WorkOrderCreate, db: Session = Depends(get_db)):
    # Añadir validaciones para asegurar que vehicle_id y client_id existan
    return crud.create_work_order(db=db, work_order=work_order)

@router.get("/by_vehicle/{vehicle_id}", response_model=List[schemas.WorkOrder])
def read_work_orders_for_vehicle(vehicle_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    work_orders = crud.get_work_orders_by_vehicle(db, vehicle_id=vehicle_id, skip=skip, limit=limit)
    return work_orders

@router.patch("/{work_order_id}", response_model=schemas.WorkOrder)
def update_work_order_status(
    work_order_id: int, 
    work_order_update: schemas.WorkOrderUpdate, 
    db: Session = Depends(get_db)
):
    updated_work_order = crud.update_work_order(db, work_order_id, work_order_update)
    if updated_work_order is None:
        raise HTTPException(status_code=404, detail="WorkOrder not found")
    return updated_work_order
