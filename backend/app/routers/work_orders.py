from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..crud import crud_work_orders, crud_vehicles
from .. import models, schemas
from ..database import get_db
from ..security import get_current_user

router = APIRouter(
    prefix="/work_orders",
    tags=["Work Orders"],
    dependencies=[Depends(get_current_user)]
)

@router.post("/", response_model=schemas.WorkOrder)
def create_work_order(
    work_order: schemas.WorkOrderCreate, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(get_current_user)
):
    """
    Crea una nueva orden de trabajo, validando la pertenencia del vehículo y cliente al tenant.
    """
    # **VALIDACIÓN CRÍTICA**: Verificamos que el vehículo exista DENTRO del tenant del usuario.
    # Esto previene crear órdenes para vehículos de otros talleres.
    vehicle = crud_vehicles.get_vehicle(db, vehicle_id=work_order.vehicle_id, tenant_id=current_user.tenant_id)
    if not vehicle:
        raise HTTPException(
            status_code=404, 
            detail=f"Vehículo con id {work_order.vehicle_id} no encontrado en tu tenant."
        )
    
    # Si bien el schema lo pide, nos aseguramos que el client_id en la orden coincida con el del vehículo.
    if vehicle.owner_id != work_order.client_id:
        raise HTTPException(
            status_code=400, # Bad Request
            detail=f"El vehículo {vehicle.id} no pertenece al cliente {work_order.client_id}."
        )

    return crud_work_orders.create_work_order(db=db, work_order=work_order)

@router.get("/", response_model=List[schemas.WorkOrder])
def read_work_orders(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Devuelve una lista de todas las órdenes de trabajo del tenant del usuario.
    """
    work_orders = crud_work_orders.get_work_orders(db, tenant_id=current_user.tenant_id, skip=skip, limit=limit)
    return work_orders

@router.get("/{work_order_id}", response_model=schemas.WorkOrder)
def read_work_order(
    work_order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Obtiene una orden de trabajo específica, verificando que pertenezca al tenant.
    """
    db_work_order = crud_work_orders.get_work_order(db, work_order_id=work_order_id, tenant_id=current_user.tenant_id)
    if db_work_order is None:
        raise HTTPException(status_code=404, detail="Orden de trabajo no encontrada")
    return db_work_order

@router.patch("/{work_order_id}", response_model=schemas.WorkOrder)
def update_work_order_status(
    work_order_id: int,
    work_order_update: schemas.WorkOrderUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Actualiza una orden de trabajo (ej. estado, costo), validando pertenencia.
    """
    # Primero, verificamos que la orden de trabajo exista y pertenezca al tenant.
    db_work_order = crud_work_orders.get_work_order(db, work_order_id=work_order_id, tenant_id=current_user.tenant_id)
    if db_work_order is None:
        raise HTTPException(status_code=404, detail="Orden de trabajo no encontrada")

    # Si existe, procedemos a actualizarla.
    return crud_work_orders.update_work_order(db=db, work_order_id=work_order_id, work_order_data=work_order_update)
