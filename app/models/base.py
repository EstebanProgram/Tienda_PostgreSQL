from sqlmodel import SQLModel, Field, Column, Numeric
from decimal import Decimal

# Clases base (para heredar)
class ProveedorBase(SQLModel):
    nombre: str = Field(index=True)
    contacto: str

class TiendaBase(SQLModel):
    nombre: str = Field(index=True)
    direccion: str

class ProductoBase(SQLModel):
    nombre: str = Field(index=True)
    precio: Decimal = Field(sa_column=Column(Numeric(10, 2)))

class TiendaProductoBase(SQLModel):
    stock: int
