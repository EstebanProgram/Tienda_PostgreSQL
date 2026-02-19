from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import ForeignKey
from .base import ProveedorBase, TiendaBase, ProductoBase, TiendaProductoBase

# Tablas ORM que usa el proyecto
class Proveedor(ProveedorBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    productos: List["Producto"] = Relationship(
        back_populates="proveedor",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "passive_deletes": True},
    )

class Tienda(TiendaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    productos: List["TiendaProducto"] = Relationship(
        back_populates="tienda",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "passive_deletes": True},
    )

class Producto(ProductoBase, table=True):
    id_producto: Optional[int] = Field(default=None, primary_key=True)
    id_proveedor: int = Field(
        sa_column=Column(ForeignKey("proveedor.id", ondelete="CASCADE"), nullable=False)
    )
    proveedor: Optional[Proveedor] = Relationship(back_populates="productos")
    tiendas: List["TiendaProducto"] = Relationship(
        back_populates="producto",
        sa_relationship_kwargs={"cascade": "all, delete-orphan", "passive_deletes": True},
    )

class TiendaProducto(TiendaProductoBase, table=True):
    id_tienda: int = Field(
        sa_column=Column(ForeignKey("tienda.id", ondelete="CASCADE"), primary_key=True)
    )
    id_producto: int = Field(
        sa_column=Column(ForeignKey("producto.id_producto", ondelete="CASCADE"), primary_key=True)
    )
    tienda: Optional[Tienda] = Relationship(back_populates="productos")
    producto: Optional[Producto] = Relationship(back_populates="tiendas")