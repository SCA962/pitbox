# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from . import models
# Importamos solo los routers que están en uso
from .routers import tenants, users, token, auth

# Crea las tablas en la base de datos (si no existen)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ERP para Talleres",
    description="API para la gestión de talleres mecánicos multi-tenant.",
    version="0.1.0",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs"
)

# --- Middlewares ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
# Monta los routers de la aplicación bajo el prefijo /api
app.include_router(auth.router, prefix="/api")
app.include_router(token.router, prefix="/api")
app.include_router(tenants.router, prefix="/api", tags=["Tenants"])
app.include_router(users.router, prefix="/api", tags=["Users"])

# --- Endpoint de Prueba de Salud ---
@app.get("/api/health-check")
def health_check():
    """
    Endpoint simple para verificar que la API está funcionando.
    """
    return {"status": "ok", "message": "Backend is running correctly"}
