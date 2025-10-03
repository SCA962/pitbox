from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, models, schemas # <--- Importamos models
from ..database import get_db
from ..security import get_current_user # <--- ¡IMPORTAMOS AL GUARDIÁN!

router = APIRouter(
    prefix="/users",
    tags=["Users"], # Corregido para consistencia
    # Podemos añadir aquí una dependencia para que TODAS las rutas de este router
    # requieran autenticación. Por ahora, lo haremos ruta por ruta.
    # dependencies=[Depends(get_current_user)]
)

# --- Endpoint de creación de usuario ---
# Este endpoint sigue siendo público, ya que alguien tiene que poder crear el primer usuario.
@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo usuario en la base de datos.
    - Verifica que el email no exista previamente.
    - La contraseña se hashea en la capa CRUD.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    return crud.create_user(db=db, user=user)


# --- Endpoint para obtener el usuario actual ---
# Este es un endpoint de prueba perfecto para el guardián.
@router.get("/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    """
    Devuelve los datos del usuario que está actualmente autenticado.
    - La dependencia `get_current_user` hace todo el trabajo de validación.
    - Si la ejecución llega aquí, significa que el token es válido.
    - La función `get_current_user` nos devuelve el objeto User de la base de datos.
    """
    return current_user


# --- Endpoint para obtener la lista de usuarios (AHORA PROTEGIDO) ---
@router.get("/", response_model=List[schemas.User])
def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # <--- ¡EL GUARDIÁN ESTÁ AQUÍ!
):
    """
    Devuelve una lista de usuarios. 
    - AHORA REQUIERE AUTENTICACIÓN.
    - El parámetro `current_user` no se usa directamente aquí, pero su mera presencia
      obliga a FastAPI a ejecutar la dependencia `get_current_user` primero.
      Si la dependencia falla, la ejecución nunca llegará al cuerpo de esta función.
    """
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
