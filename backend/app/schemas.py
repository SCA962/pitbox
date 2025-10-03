from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

# -------- Auth --------
# Schema para el registro de un nuevo Tenant
class TenantRegistration(BaseModel):
    workshop_name: str
    admin_email: EmailStr
    admin_password: str

# -------- Tenant --------
class TenantBase(BaseModel):
    name: str

class TenantCreate(TenantBase):
    pass

class Tenant(TenantBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

# -------- User --------
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str
    tenant_id: int
    is_admin: bool = False # Por defecto, los usuarios no son admins

class User(UserBase):
    id: int
    is_active: bool
    is_admin: bool
    tenant_id: int

    class Config:
        orm_mode = True

# -------- Client --------
class ClientBase(BaseModel):
    full_name: str
    email: Optional[EmailStr] = None
    phone_number: str

# El 'tenant_id' ya no se pasa en el body. Se infiere del usuario autenticado.
class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    tenant_id: int

    class Config:
        orm_mode = True

# -------- Vehicle --------
class VehicleBase(BaseModel):
    make: str
    model: str
    year: int
    license_plate: str

class VehicleCreate(VehicleBase):
    owner_id: int

class Vehicle(VehicleBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

# -------- WorkOrder --------
class WorkOrderBase(BaseModel):
    description: str
    status: Optional[str] = "Pending"

class WorkOrderCreate(WorkOrderBase):
    vehicle_id: int
    client_id: int

class WorkOrderUpdate(BaseModel):
    description: Optional[str] = None
    status: Optional[str] = None
    total_cost: Optional[float] = None

class WorkOrder(WorkOrderBase):
    id: int
    total_cost: float
    created_at: datetime
    vehicle_id: int
    client_id: int

    class Config:
        orm_mode = True

# -------- Token --------
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
