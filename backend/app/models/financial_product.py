from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean, DateTime
from sqlalchemy.sql import func
from ..database import Base

class FinancialProduct(Base):
    __tablename__ = "financial_products"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, index=True)
    type = Column(String)  # cuenta, tarjeta_credito, prestamo, inversion
    institution = Column(String)
    balance = Column(Float, default=0.0)
    currency = Column(String, default="MXN")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

# Esquema Pydantic para validación de datos
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class FinancialProductBase(BaseModel):
    name: str
    type: str = Field(..., description="Tipo de producto: cuenta, tarjeta_credito, prestamo, inversion")
    institution: str
    balance: float = Field(default=0.0)
    currency: str = Field(default="MXN")
    is_active: bool = Field(default=True)

class FinancialProductCreate(FinancialProductBase):
    pass

class FinancialProductResponse(FinancialProductBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True 