from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud, models
from ..database import get_db
from ..security import get_current_user, create_access_token, verify_password

# Router para operaciones de registro y login (no requiere token)
router = APIRouter(
    tags=["Auth"],
)

# 1. Se cambia el schema esperado a TenantRegistration para que coincida con el formulario del frontend.
# 2. Se actualiza la lógica para crear tanto el Tenant como el primer Usuario (admin).
@router.post("/register", response_model=schemas.User) # Devuelve el usuario creado, no el tenant
def register_tenant_and_admin_user(registration_data: schemas.TenantRegistration, db: Session = Depends(get_db)):
    """
    Registra un nuevo Tenant y su usuario administrador inicial.
    Este es el endpoint que debe ser llamado desde el formulario de registro.
    """
    # Validar si el nombre del taller ya existe
    db_tenant = crud.get_tenant_by_name(db, name=registration_data.workshop_name)
    if db_tenant:
        raise HTTPException(status_code=400, detail="Workshop name already registered")

    # Validar si el email del admin ya existe
    db_user = crud.get_user_by_email(db, email=registration_data.admin_email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Crear el nuevo Tenant (Taller)
    new_tenant = crud.create_tenant(db=db, tenant=schemas.TenantCreate(name=registration_data.workshop_name))

    # Preparar los datos para el nuevo usuario admin
    user_data = schemas.UserCreate(
        email=registration_data.admin_email,
        password=registration_data.admin_password,
        tenant_id=new_tenant.id,
        is_admin=True  # El primer usuario es siempre el admin
    )

    # Crear el usuario administrador
    new_user = crud.create_user(db=db, user=user_data)
    
    return new_user


# Router protegido (requiere token)
protected_router = APIRouter(
    dependencies=[Depends(get_current_user)],
    tags=["Protected Auth Endpoints"]
)

@protected_router.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    """
    Endpoint de prueba para verificar que el token funciona.
    Devuelve los datos del usuario correspondiente al token.
    """
    return current_user
