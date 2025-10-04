from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import crud, schemas
from app.database import get_db
from ..security import verify_password, create_access_token

# Creamos un nuevo router para gestionar la autenticación y la emisión de tokens
router = APIRouter(
    tags=["Authentication"], # Etiqueta para agrupar en la documentación
)

# --- Endpoint de Autenticación y Creación de Token ---
@router.post("/token", response_model=schemas.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Este es el endpoint de login. 
    - Utiliza el flujo estándar de OAuth2 para recibir el usuario y la contraseña.
    - Busca al usuario en la base de datos.
    - Verifica que la contraseña sea correcta.
    - Si todo es válido, crea y devuelve un token de acceso JWT.
    """
    # 1. Buscamos al usuario por su email (que en OAuth2 se llama 'username')
    user = crud.get_user_by_email(db, email=form_data.username)

    # 2. Verificamos si el usuario existe y si la contraseña es correcta
    # Usamos la función 'verify_password' que creamos en security.py
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"}, # Estándar para errores de autenticación
        )

    # 3. Si las credenciales son válidas, creamos el token de acceso
    # El "sub" (subject) del token será el email del usuario. Podríamos añadir más datos.
    access_token = create_access_token(
        data={"sub": user.email}
    )

    # 4. Devolvemos el token en la respuesta
    return {"access_token": access_token, "token_type": "bearer"}
