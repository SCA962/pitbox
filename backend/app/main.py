from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from . import models
from .routers import tenants, users, clients, vehicles, work_orders

# Crea las tablas en la base de datos (si no existen)
# En un entorno de producción, es preferible usar migraciones con Alembic
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ERP para Talleres",
    description="API para la gestión de talleres mecánicos multi-tenant.",
    version="0.1.0",
)

# --- Middlewares ---
# Configuración de CORS para permitir que el frontend se comunique con el backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"], # Origen de tu app de React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
# Incluir los routers de las diferentes entidades de la aplicación
app.include_router(tenants.router)
app.include_router(users.router)
app.include_router(clients.router)
app.include_router(vehicles.router)
app.include_router(work_orders.router)

# --- Rutas base ---
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido al API del ERP para Talleres"}

@app.get("/health", tags=["Health Check"])
async def health_check():
    return {"status": "ok"}
