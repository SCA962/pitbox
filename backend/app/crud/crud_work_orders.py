from sqlalchemy.orm import Session

from .. import models, schemas

# --- WorkOrder --- 

def get_work_order(db: Session, work_order_id: int, tenant_id: int):
    return (db.query(models.WorkOrder)
              .join(models.Vehicle, models.WorkOrder.vehicle_id == models.Vehicle.id)
              .join(models.Client, models.Vehicle.owner_id == models.Client.id)
              .filter(models.WorkOrder.id == work_order_id, models.Client.tenant_id == tenant_id)
              .first())

def get_work_orders(db: Session, tenant_id: int, skip: int = 0, limit: int = 100):
    return (db.query(models.WorkOrder)
              .join(models.Vehicle, models.WorkOrder.vehicle_id == models.Vehicle.id)
              .join(models.Client, models.Vehicle.owner_id == models.Client.id)
              .filter(models.Client.tenant_id == tenant_id)
              .offset(skip).limit(limit).all())

def create_work_order(db: Session, work_order: schemas.WorkOrderCreate):
    db_work_order = models.WorkOrder(**work_order.dict())
    db.add(db_work_order)
    db.commit()
    db.refresh(db_work_order)
    return db_work_order

def update_work_order(db: Session, work_order_id: int, work_order_data: schemas.WorkOrderUpdate):
    # La validación de pertenencia se hará en el router antes de llamar aquí
    db_work_order = db.query(models.WorkOrder).filter(models.WorkOrder.id == work_order_id).first()
    if not db_work_order:
        return None
    update_data = work_order_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_work_order, key, value)
    db.commit()
    db.refresh(db_work_order)
    return db_work_order
