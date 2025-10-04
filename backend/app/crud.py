from sqlalchemy.orm import Session
from . import models, schemas
from .security import get_password_hash

# ----> INICIO: Funciones CRUD para Tenant <----

def get_tenant(db: Session, tenant_id: int):
    """Obtiene un tenant por su ID."""
    return db.query(models.Tenant).filter(models.Tenant.id == tenant_id).first()

def get_tenant_by_name(db: Session, name: str):
    """Obtiene un tenant por su nombre."""
    return db.query(models.Tenant).filter(models.Tenant.name == name).first()

def get_tenants(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de tenants."""
    return db.query(models.Tenant).offset(skip).limit(limit).all()

def create_tenant(db: Session, tenant: schemas.TenantCreate) -> models.Tenant:
    """Crea un nuevo tenant."""
    db_tenant = models.Tenant(name=tenant.name)
    db.add(db_tenant)
    db.commit()
    db.refresh(db_tenant)
    return db_tenant

# ----> FIN: Funciones CRUD para Tenant <----


# ----> INICIO: Funciones CRUD para User <----

def get_user(db: Session, user_id: int):
    """Obtiene un usuario por su ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """Obtiene un usuario por su email."""
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    """Obtiene una lista de usuarios."""
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Crea un nuevo usuario con contraseña hasheada."""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email, 
        hashed_password=hashed_password,
        tenant_id=user.tenant_id,
        is_admin=user.is_admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    
# ----> FIN: Funciones CRUD para User <----
