# backend/app/config.py
from pydantic_settings import BaseSettings
from pydantic import validator
from typing import Dict, Any

class Settings(BaseSettings):
    # Estas son las variables que leeremos del archivo .env
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_DB: str

    # Esta variable la construiremos nosotros, no está en el .env
    DATABASE_URL: str = ""

    # Esta función mágica construye la URL de la base de datos
    # a partir de las otras variables, justo después de leerlas.
    @validator("DATABASE_URL", pre=True, always=True)
    def assemble_db_connection(cls, v: str, values: Dict[str, Any]) -> str:
        if v:
            return v
        return (
            f"postgresql://{values.get('POSTGRES_USER')}:{values.get('POSTGRES_PASSWORD')}"
            f"@{values.get('POSTGRES_SERVER')}/{values.get('POSTGRES_DB')}"
        )

    class Config:
        # Le decimos a Pydantic que cargue las variables desde este archivo
        env_file = ".env"
        env_file_encoding = "utf-8"

# Creamos una única instancia de la configuración para toda la app
settings = Settings()
