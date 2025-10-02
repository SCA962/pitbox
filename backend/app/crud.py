from sqlalchemy.orm import Session
from . import models, schemas
import passlib.hash as _hash

# Hashing de contraseñas
def get_password_hash(password):
    return _hash.bcrypt.hash(password)

# --- Tenant --- 

def get_tenant(db: Session, tenant_id: int):
    return db.query(models.Tenant).filter(models.Tenant.id == tenant_id).first()

def get_tenant_by_name(db: Session, name: str):
    return db.query(models.Tenant).filter(models.Tenant.name == name).first()

def get_tenants(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Tenant).offset(skip).limit(limit).all()

def create_tenant(db: Session, tenant: schemas.TenantCreate):
    db_tenant = models.Tenant(name=tenant.name)
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return db_tenant

# --- User --- 

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password, tenant_id=user.tenant_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Client --- 

def get_client(db: Session, client_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id).first()

def get_clients(db: Session, tenant_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Client).filter(models.Client.tenant_id == tenant_id).offset(skip).limit(limit).all()

def create_client(db: Session, client: schemas.ClientCreate):
    db_client = models.Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

# --- Vehicle --- 

def get_vehicle(db: Session, vehicle_id: int):
    return db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()

def get_vehicles_by_client(db: Session, client_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Vehicle).filter(models.Vehicle.owner_id == client_id).offset(skip).limit(limit).all()

def create_vehicle(db: Session, vehicle: schemas.VehicleCreate):
    db_vehicle = models.Vehicle(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

# --- WorkOrder --- 

def get_work_order(db: Session, work_order_id: int):
    return db.query(models.WorkOrder).filter(models.WorkOrder.id == work_order_id).first()

def get_work_orders_by_vehicle(db: Session, vehicle_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.WorkOrder).filter(models.WorkOrder.vehicle_id == vehicle_id).offset(skip).limit(limit).all()

def create_work_order(db: Session, work_order: schemas.WorkOrderCreate):
    db_work_order = models.WorkOrder(**work_order.dict())
    db.add(db_work_order)
    db.commit()
    db.refresh(db_work_order)
    return db_work_order

def update_work_order(db: Session, work_order_id: int, work_order_data: schemas.WorkOrderUpdate):
    db_work_order = get_work_order(db, work_order_id)
    if not db_work_order:
        return None
    update_data = work_order_data.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_work_order, key, value)
    db.commit()
    db.refresh(db_work_order)
    return db_work_order
