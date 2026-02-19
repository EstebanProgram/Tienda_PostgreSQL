# Aqui uso __init__.py para convertir un directorio en paquete y exponer funciones y clases de sus modulos
from .tables import Proveedor, Tienda, Producto, TiendaProducto
from .schemas import (
    ProveedorPublic, TiendaPublic, ProductoPublic, TiendaProductoPublic, TiendaProductoDetalle,
    ProductoCreate, ProductoUpdate, TiendaProductoUpdate, ProveedorUpdate, TiendaUpdate
)
from .base import ProveedorBase, TiendaBase, ProductoBase, TiendaProductoBase