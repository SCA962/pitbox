from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine
from . import models
from .routers import tenants, users, clients, vehicles, work_orders

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
# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
# Se añade el prefijo /api a todos los routers para que coincidan con el proxy de Vite
app.include_router(tenants.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(clients.router, prefix="/api")
app.include_router(vehicles.router, prefix="/api")
app.include_router(work_orders.router, prefix="/api")

# --- Rutas base ---
@app.get("/api", tags=["Root"])
def read_root():
    return {"message": "Bienvenido al API del ERP para Talleres"}

@app.get("/api/health", tags=["Health Check"])
async def health_check():
    # Esta es la ruta que el frontend está esperando
    return {"status": "ok"}

# La ruta @app.get("/") que existía antes ya no es necesaria
# ya que hemos movido la raíz a /api
