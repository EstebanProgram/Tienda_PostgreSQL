from sqlmodel import SQLModel
from .session import engine
from models.tables import Proveedor, Tienda, Producto, TiendaProducto

# Crea todas las tablas en la base de datos segu los modelos ORM.
def init_db():
    SQLModel.metadata.create_all(engine)