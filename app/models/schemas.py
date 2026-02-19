from decimal import Decimal
from sqlmodel import SQLModel
from typing import Optional

# Squemas publicos
class ProveedorPublic(SQLModel):
    id: int
    nombre: str
    contacto: str

class TiendaPublic(SQLModel):
    id: int
    nombre: str
    direccion: str

class ProductoPublic(SQLModel):
    id_producto: int
    id_proveedor: int
    nombre: str
    precio: Decimal

class TiendaProductoPublic(SQLModel):
    id_tienda: int
    id_producto: int
    stock: int

class TiendaProductoDetalle(TiendaProductoPublic):
    nombre_producto: str
    precio: Decimal

# Squemas de creacion
class ProductoCreate(SQLModel):
    nombre: str
    precio: Decimal
    id_proveedor: int

# squemas de actualizacion
class ProveedorUpdate(SQLModel):
    nombre: Optional[str] = None
    contacto: Optional[str] = None

class TiendaUpdate(SQLModel):
    nombre: Optional[str] = None
    direccion: Optional[str] = None

class ProductoUpdate(SQLModel):
    nombre: Optional[str] = None
    precio: Optional[Decimal] = None

class TiendaProductoUpdate(SQLModel):
    stock: Optional[int] = None
