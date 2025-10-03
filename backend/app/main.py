# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from . import models
from .routers import tenants, users, clients, vehicles, work_orders, token # <--- IMPORTAMOS EL NUEVO ROUTER

# Crea las tablas en la base de datos (si no existen)
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ERP para Talleres",
    description="API para la gestión de talleres mecánicos multi-tenant.",
    version="0.1.0",
    # La URL de la especificación OpenAPI también debe estar bajo /api
    openapi_url="/api/openapi.json",
    # La URL de la documentación interactiva (Swagger) se servirá en /api/docs
    docs_url="/api/docs"
)

# --- Middlewares ---
# Configuración de CORS para permitir que el frontend se conecte
app.add_middleware(
    CORSMiddleware,
    # Permitimos todos los orígenes para el entorno de demo
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
# Monta todos los routers de la aplicación bajo el prefijo /api
app.include_router(token.router, prefix="/api") # <--- AÑADIMOS EL ROUTER DE TOKEN
app.include_router(tenants.router, prefix="/api", tags=["Tenants"])
app.include_router(users.router, prefix="/api", tags=["Users"])
app.include_router(clients.router, prefix="/api", tags=["Clients"])
app.include_router(vehicles.router, prefix="/api", tags=["Vehicles"])
app.include_router(work_orders.router, prefix="/api", tags=["Work Orders"])

# --- Endpoint de Prueba de Salud ---
# Esta es la ruta que el frontend usará para verificar si el backend está vivo.
@app.get("/api/health-check")
def health_check():
    """
    Endpoint simple para verificar que la API está funcionando.
    """
    return {"status": "ok", "message": "Backend is running correctly"}
