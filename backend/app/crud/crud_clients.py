from sqlalchemy.orm import Session

from .. import models, schemas

# --- Client --- 

def get_client(db: Session, client_id: int, tenant_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id, models.Client.tenant_id == tenant_id).first()

def get_clients(db: Session, tenant_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Client).filter(models.Client.tenant_id == tenant_id).offset(skip).limit(limit).all()

def create_client(db: Session, client: schemas.ClientCreate, tenant_id: int):
    db_client = models.Client(**client.dict(), tenant_id=tenant_id)
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client
