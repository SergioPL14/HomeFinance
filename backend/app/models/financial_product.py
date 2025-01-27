from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
import enum
from ..database import Base

class ProductType(enum.Enum):
    BANK_ACCOUNT = "bank_account"
    INVESTMENT_FUND = "investment_fund"
    CRYPTO = "cryptocurrency"

class FinancialProduct(Base):
    __tablename__ = "financial_products"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    type = Column(String)
    provider = Column(String)  # Santander, Evo, Revolut, etc.
    identifier = Column(String)  # ID externo del producto
    balance = Column(Float)
    currency = Column(String)
    last_updated = Column(String)  # Timestamp 