import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import get_db

# --- Carga de Variables de Entorno ---
load_dotenv()

# --- Configuración de Seguridad para Tokens (JWT) ---
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# Esta es una utilidad de FastAPI que sabe cómo buscar un token. 
# Le indicamos que la URL para obtener el token es "/api/token".
# Cuando la usemos en una dependencia, buscará en la petición una cabecera
# "Authorization" con el formato "Bearer <token>".
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token")

# --- Configuración de Hashing de Contraseñas ---
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# --- Funciones de Utilidad de Seguridad ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Dependencia de Seguridad Principal (El Guardián) ---
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    """
    Esta es la dependencia "guardián". Se inyecta en los endpoints que requieren protección.

    1. Depende de `oauth2_scheme`, que extrae el token de la cabecera Authorization.
    2. Decodifica y valida el token JWT.
    3. Extrae el email del usuario del payload del token.
    4. Busca y devuelve el usuario de la base de datos.
    5. Lanza excepciones HTTP si algo falla (token inválido, usuario no encontrado, etc.).
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Intentamos decodificar el token usando nuestra clave secreta y algoritmo
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Extraemos el email del campo "sub" (subject)
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        # Validamos el formato de los datos del token con nuestro schema
        token_data = schemas.TokenData(email=email)
    except JWTError:
        # Si el token está mal formado, ha expirado o la firma es inválida, lanzamos error
        raise credentials_exception

    # Buscamos al usuario en la base de datos a partir del email del token
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        # Si el token es válido pero el usuario ya no existe en la DB
        raise credentials_exception
    
    # Si todo ha ido bien, devolvemos el objeto User completo
    return user
