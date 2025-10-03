from sqlalchemy.orm import Session

from .. import models, schemas

# --- Vehicle --- 

def get_vehicle(db: Session, vehicle_id: int, tenant_id: int):
    return (db.query(models.Vehicle)
              .join(models.Client, models.Vehicle.owner_id == models.Client.id)
              .filter(models.Vehicle.id == vehicle_id, models.Client.tenant_id == tenant_id)
              .first())

def get_vehicles(db: Session, tenant_id: int, skip: int = 0, limit: int = 100):
    return (db.query(models.Vehicle)
              .join(models.Client, models.Vehicle.owner_id == models.Client.id)
              .filter(models.Client.tenant_id == tenant_id)
              .offset(skip).limit(limit).all())

def create_vehicle(db: Session, vehicle: schemas.VehicleCreate):
    db_vehicle = models.Vehicle(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle
