from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    users = relationship("User", back_populates="tenant")
    clients = relationship("Client", back_populates="tenant")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))

    tenant = relationship("Tenant", back_populates="users")

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, index=True)
    phone_number = Column(String)
    tenant_id = Column(Integer, ForeignKey("tenants.id"))

    tenant = relationship("Tenant", back_populates="clients")
    vehicles = relationship("Vehicle", back_populates="owner")

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True, index=True)
    make = Column(String) # Marca (ej. Toyota)
    model = Column(String) # Modelo (ej. Corolla)
    year = Column(Integer)
    license_plate = Column(String, unique=True, index=True) # Matrícula
    owner_id = Column(Integer, ForeignKey("clients.id"))

    owner = relationship("Client", back_populates="vehicles")
    work_orders = relationship("WorkOrder", back_populates="vehicle")

class WorkOrder(Base):
    __tablename__ = "work_orders"
    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    status = Column(String, default="Pending") # Pending, In-Progress, Completed, Cancelled
    total_cost = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    client_id = Column(Integer, ForeignKey("clients.id")) # Para referencia rápida

    vehicle = relationship("Vehicle", back_populates="work_orders")
    client = relationship("Client")
