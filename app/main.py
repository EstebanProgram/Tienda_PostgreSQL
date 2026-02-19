from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import SQLModel, create_engine, Session, select
from typing import Annotated
from decimal import Decimal

from .config import settings
from .models import (
    Proveedor, Tienda, Producto, TiendaProducto,
    ProveedorBase, TiendaBase, ProductoBase, TiendaProductoBase,
    ProveedorPublic, TiendaPublic, ProductoPublic, TiendaProductoPublic,
    ProductoCreate, ProveedorUpdate, TiendaUpdate, ProductoUpdate, TiendaProductoUpdate,
    TiendaProductoDetalle
)

# Configuracion de la DB
postgres_url = (
    f"postgresql+psycopg2://{settings.POSTGRES_USER}:"
    f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:"
    f"{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)
engine = create_engine(postgres_url, echo=settings.DEBUG)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

# App FastAPI
app = FastAPI(title="Tienda API")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Endpoints proveedores
@app.post("/proveedores/", response_model=ProveedorPublic)
def create_proveedor(proveedor: ProveedorBase, session: SessionDep):
    db_proveedor = Proveedor(**proveedor.model_dump())
    session.add(db_proveedor)
    session.commit()
    session.refresh(db_proveedor)
    return db_proveedor

@app.get("/proveedores/", response_model=list[ProveedorPublic])
def read_proveedores(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    return session.exec(select(Proveedor).offset(offset).limit(limit)).all()

@app.get("/proveedores/{proveedor_id}", response_model=ProveedorPublic)
def read_proveedor(proveedor_id: int, session: SessionDep):
    proveedor = session.get(Proveedor, proveedor_id)
    if not proveedor:
        raise HTTPException(404, "Proveedor no encontrado")
    return proveedor

@app.get("/proveedores/nombre/", response_model=list[ProveedorPublic])
def read_proveedor_por_nombre(nombre: str, session: SessionDep):
    proveedores = session.exec(select(Proveedor).where(Proveedor.nombre.ilike(f"%{nombre}%"))).all()
    if not proveedores:
        raise HTTPException(404, "No se encontraron proveedores")
    return proveedores

@app.patch("/proveedores/{proveedor_id}", response_model=ProveedorPublic)
def update_proveedor(proveedor_id: int, proveedor: ProveedorUpdate, session: SessionDep):
    proveedor_db = session.get(Proveedor, proveedor_id)
    if not proveedor_db:
        raise HTTPException(404, "Proveedor no encontrado")
    for key, value in proveedor.model_dump(exclude_unset=True).items():
        setattr(proveedor_db, key, value)
    session.commit()
    session.refresh(proveedor_db)
    return proveedor_db

@app.delete("/proveedores/{proveedor_id}")
def delete_proveedor(proveedor_id: int, session: SessionDep):
    proveedor = session.get(Proveedor, proveedor_id)
    if not proveedor:
        raise HTTPException(404, "Proveedor no encontrado")
    session.delete(proveedor)
    session.commit()
    return {"ok": True}

# Endpoints tiendas
@app.post("/tiendas/", response_model=TiendaPublic)
def create_tienda(tienda: TiendaBase, session: SessionDep):
    db_tienda = Tienda(**tienda.model_dump())
    session.add(db_tienda)
    session.commit()
    session.refresh(db_tienda)
    return db_tienda

@app.get("/tiendas/", response_model=list[TiendaPublic])
def read_tiendas(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    return session.exec(select(Tienda).offset(offset).limit(limit)).all()

@app.get("/tiendas/{tienda_id}", response_model=TiendaPublic)
def read_tienda(tienda_id: int, session: SessionDep):
    tienda = session.get(Tienda, tienda_id)
    if not tienda:
        raise HTTPException(404, "Tienda no encontrada")
    return tienda

@app.get("/tiendas/nombre/", response_model=list[TiendaPublic])
def read_tienda_por_nombre(nombre: str, session: SessionDep):
    tiendas = session.exec(select(Tienda).where(Tienda.nombre.ilike(f"%{nombre}%"))).all()
    if not tiendas:
        raise HTTPException(404, "No se encontraron tiendas")
    return tiendas

@app.patch("/tiendas/{tienda_id}", response_model=TiendaPublic)
def update_tienda(tienda_id: int, tienda: TiendaUpdate, session: SessionDep):
    tienda_db = session.get(Tienda, tienda_id)
    if not tienda_db:
        raise HTTPException(404, "Tienda no encontrada")
    for key, value in tienda.model_dump(exclude_unset=True).items():
        setattr(tienda_db, key, value)
    session.commit()
    session.refresh(tienda_db)
    return tienda_db

@app.delete("/tiendas/{tienda_id}")
def delete_tienda(tienda_id: int, session: SessionDep):
    tienda = session.get(Tienda, tienda_id)
    if not tienda:
        raise HTTPException(404, "Tienda no encontrada")
    session.delete(tienda)
    session.commit()
    return {"ok": True}

# Endpoints producto
@app.post("/productos/", response_model=ProductoPublic)
def create_producto(producto: ProductoCreate, session: SessionDep):
    proveedor = session.get(Proveedor, producto.id_proveedor)
    if not proveedor:
        raise HTTPException(404, "Proveedor no existe")
    db_producto = Producto(**producto.model_dump())
    session.add(db_producto)
    session.commit()
    session.refresh(db_producto)
    return db_producto

@app.get("/productos/", response_model=list[ProductoPublic])
def read_productos(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100):
    return session.exec(select(Producto).offset(offset).limit(limit)).all()

@app.get("/productos/{producto_id}", response_model=ProductoPublic)
def read_producto(producto_id: int, session: SessionDep):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(404, "Producto no encontrado")
    return producto

@app.get("/productos/nombre/", response_model=list[ProductoPublic])
def read_producto_por_nombre(nombre: str, session: SessionDep):
    productos = session.exec(select(Producto).where(Producto.nombre.ilike(f"%{nombre}%"))).all()
    if not productos:
        raise HTTPException(404, "No se encontraron productos")
    return productos

@app.patch("/productos/{producto_id}", response_model=ProductoPublic)
def update_producto(producto_id: int, producto: ProductoUpdate, session: SessionDep):
    producto_db = session.get(Producto, producto_id)
    if not producto_db:
        raise HTTPException(404, "Producto no encontrado")
    for key, value in producto.model_dump(exclude_unset=True).items():
        setattr(producto_db, key, value)
    session.commit()
    session.refresh(producto_db)
    return producto_db

@app.delete("/productos/{producto_id}")
def delete_producto(producto_id: int, session: SessionDep):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(404, "Producto no encontrado")
    session.delete(producto)
    session.commit()
    return {"ok": True}


# Endpoints relacion tienda-producto
@app.post("/tiendas/{tienda_id}/productos/{producto_id}", response_model=TiendaProductoPublic)
def add_producto_a_tienda(tienda_id: int, producto_id: int, data: TiendaProductoBase, session: SessionDep):
    tienda = session.get(Tienda, tienda_id)
    if not tienda:
        raise HTTPException(404, "Tienda no existe")
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(404, "Producto no existe")
    relacion = TiendaProducto(stock=data.stock)
    relacion.tienda = tienda
    relacion.producto = producto
    session.add(relacion)
    session.commit()
    session.refresh(relacion)
    return relacion

@app.get("/tiendas/{tienda_id}/productos", response_model=list[TiendaProductoDetalle])
def get_productos_de_tienda(tienda_id: int, session: SessionDep):
    tienda = session.get(Tienda, tienda_id)
    if not tienda:
        raise HTTPException(404, "Tienda no existe")
    return [
        TiendaProductoDetalle(
            id_tienda=tp.id_tienda,
            id_producto=tp.id_producto,
            stock=tp.stock,
            nombre_producto=tp.producto.nombre,
            precio=tp.producto.precio,
        )
        for tp in tienda.productos
    ]

@app.patch("/tiendas/{tienda_id}/productos/{producto_id}", response_model=TiendaProductoPublic)
def update_stock(tienda_id: int, producto_id: int, stock_update: TiendaProductoUpdate, session: SessionDep):
    relacion = session.get(TiendaProducto, (tienda_id, producto_id))
    if not relacion:
        raise HTTPException(404, "El producto no está en la tienda")
    if stock_update.stock is not None:
        relacion.stock = stock_update.stock
    session.commit()
    session.refresh(relacion)
    return relacion

@app.delete("/tiendas/{tienda_id}/productos/{producto_id}")
def delete_producto_de_tienda(tienda_id: int, producto_id: int, session: SessionDep):
    relacion = session.get(TiendaProducto, (tienda_id, producto_id))
    if not relacion:
        raise HTTPException(404, "El producto no está en la tienda")
    session.delete(relacion)
    session.commit()
    return {"ok": True}