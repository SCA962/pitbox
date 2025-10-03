
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import database, models, schemas, crud
from ..dependencies import get_db
from passlib.context import CryptContext

# Configuración para el hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def register_new_tenant(registration_data: schemas.TenantRegistration, db: Session = Depends(get_db)):
    """
    Registra un nuevo tenant (taller) y su usuario administrador.

    - **workshop_name**: Nombre del nuevo taller.
    - **admin_email**: Email del usuario administrador.
    - **admin_password**: Contraseña del usuario administrador.
    """
    # 1. Verificar si ya existe un usuario con ese email
    db_user = crud.get_user_by_email(db, email=registration_data.admin_email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # 2. Hashear la contraseña antes de guardarla
    hashed_password = pwd_context.hash(registration_data.admin_password)

    # 3. Crear el nuevo Tenant en la base de datos
    new_tenant = crud.create_tenant(db=db, tenant=schemas.TenantBase(name=registration_data.workshop_name))

    # 4. Crear el usuario administrador asociado al nuevo tenant
    user_to_create = schemas.UserCreate(
        email=registration_data.admin_email,
        password=hashed_password,
        tenant_id=new_tenant.id,
        is_admin=True # El primer usuario de un tenant es siempre admin
    )
    new_user = crud.create_user(db=db, user=user_to_create)

    return new_user
