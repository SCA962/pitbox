from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud, models
# Corrección: Se importa get_db desde database, no dependencies
from ..database import get_db 
from ..security import get_current_user, create_access_token, verify_password

# Router para operaciones de registro y login (no requiere token)
router = APIRouter(
    tags=["Auth"],
)

@router.post("/register/tenant", response_model=schemas.Tenant)
def register_tenant(tenant: schemas.TenantCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo Tenant (taller) en el sistema.
    Este es el primer paso para un nuevo cliente (taller).
    """
    db_tenant = crud.get_tenant_by_name(db, name=tenant.name)
    if db_tenant:
        raise HTTPException(status_code=400, detail="Tenant name already registered")
    return crud.create_tenant(db=db, tenant=tenant)


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
