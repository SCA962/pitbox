from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import schemas, crud, models
from ..database import get_db
from ..security import get_current_user, create_access_token, verify_password
from datetime import timedelta

# Router para operaciones de registro y login (no requiere token)
router = APIRouter(
    tags=["Auth"],
)

# Endpoint de Registro
@router.post("/register", response_model=schemas.User)
def register_tenant_and_admin_user(registration_data: schemas.TenantRegistration, db: Session = Depends(get_db)):
    """
    Registra un nuevo Tenant y su usuario administrador inicial.
    """
    db_tenant = crud.get_tenant_by_name(db, name=registration_data.workshop_name)
    if db_tenant:
        raise HTTPException(status_code=400, detail="Workshop name already registered")

    db_user = crud.get_user_by_email(db, email=registration_data.admin_email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_tenant = crud.create_tenant(db=db, tenant=schemas.TenantCreate(name=registration_data.workshop_name))

    user_data = schemas.UserCreate(
        email=registration_data.admin_email,
        password=registration_data.admin_password,
        tenant_id=new_tenant.id,
        is_admin=True
    )
    new_user = crud.create_user(db=db, user=user_data)
    
    return new_user

# Endpoint de Login (Token)
@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Proporciona un token de acceso a partir de email y contraseña.
    El frontend debe enviar los datos como 'x-www-form-urlencoded'.
    """
    # Busca al usuario por su email (que llega en el campo 'username' del form)
    user = crud.get_user_by_email(db, email=form_data.username)
    
    # Si el usuario no existe o la contraseña es incorrecta, deniega el acceso
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Si las credenciales son válidas, crea un token de acceso
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


# Router protegido (requiere token)
protected_router = APIRouter(
    dependencies=[Depends(get_current_user)],
    tags=["Protected Auth Endpoints"]
)

@protected_router.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    """
    Endpoint de prueba para verificar que el token funciona.
    """
    return current_user
