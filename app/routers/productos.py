from fastapi import APIRouter, HTTPException
from sqlmodel import select
from db.session import SessionDep
from models.tables import Producto, Proveedor, TiendaProducto, Tienda
from models.schemas import ProductoPublic, ProductoUpdate, ProductoCreate, TiendaProductoPublic, TiendaProductoUpdate, TiendaProductoBase, TiendaProductoDetalle

router = APIRouter(prefix="/productos", tags=["productos"])

# Crear producto
@router.post("/", response_model=ProductoPublic)
def create_producto(producto: ProductoCreate, session: SessionDep):
    proveedor = session.get(Proveedor, producto.id_proveedor)
    if not proveedor:
        raise HTTPException(404, "Proveedor no existe")
    db_producto = Producto(nombre=producto.nombre, precio=producto.precio, proveedor=proveedor)
    session.add(db_producto)
    session.commit()
    session.refresh(db_producto)
    return db_producto

# Leer todos los productos
@router.get("/", response_model=list[ProductoPublic])
def read_productos(session: SessionDep):
    return session.exec(select(Producto)).all()

# Leer por ID
@router.get("/{producto_id}", response_model=ProductoPublic)
def read_producto(producto_id: int, session: SessionDep):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(404, "Producto no encontrado")
    return producto

# Leer por nombre (like)
@router.get("/nombre/", response_model=list[ProductoPublic])
def read_producto_por_nombre(nombre: str, session: SessionDep):
    productos = session.exec(select(Producto).where(Producto.nombre.ilike(f"%{nombre}%"))).all()
    if not productos:
        raise HTTPException(404, "No se encontraron productos con ese nombre")
    return productos

# Actualizar producto
@router.patch("/{producto_id}", response_model=ProductoPublic)
def update_producto(producto_id: int, producto: ProductoUpdate, session: SessionDep):
    producto_db = session.get(Producto, producto_id)
    if not producto_db:
        raise HTTPException(404, "Producto no encontrado")
    data = producto.model_dump(exclude_unset=True)
    producto_db.sqlmodel_update(data)
    session.commit()
    session.refresh(producto_db)
    return producto_db

# Eliminar producto
@router.delete("/{producto_id}")
def delete_producto(producto_id: int, session: SessionDep):
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(404, "Producto no encontrado")
    session.delete(producto)
    session.commit()
    return {"ok": True}

# Gestion de productos en tienda  /
# -------------------------------/

# Agregar producto a tienda
@router.post("/tiendas/{tienda_id}/productos/{producto_id}", response_model=TiendaProductoPublic)
def add_producto_a_tienda(tienda_id: int, producto_id: int, data: TiendaProductoBase, session: SessionDep):
    tienda = session.get(Tienda, tienda_id)
    if not tienda:
        raise HTTPException(404, "Tienda no existe")
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(404, "Producto no existe")
    relacion = TiendaProducto(tienda=tienda, producto=producto, stock=data.stock)
    session.add(relacion)
    session.commit()
    session.refresh(relacion)
    return relacion

# Actualizar stock
@router.patch("/tiendas/{tienda_id}/productos/{producto_id}", response_model=TiendaProductoPublic)
def update_stock(tienda_id: int, producto_id: int, stock_update: TiendaProductoUpdate, session: SessionDep):
    relacion = session.get(TiendaProducto, (tienda_id, producto_id))
    if not relacion:
        raise HTTPException(404, "El producto no está en la tienda")
    if stock_update.stock is not None:
        relacion.stock = stock_update.stock
    session.commit()
    session.refresh(relacion)
    return relacion

# Eliminar producto de tienda
@router.delete("/tiendas/{tienda_id}/productos/{producto_id}")
def delete_producto_de_tienda(tienda_id: int, producto_id: int, session: SessionDep):
    relacion = session.get(TiendaProducto, (tienda_id, producto_id))
    if not relacion:
        raise HTTPException(404, "El producto no está en la tienda")
    session.delete(relacion)
    session.commit()
    return {"ok": True}

# Listar productos de una tienda
@router.get("/tiendas/{tienda_id}/productos", response_model=list[TiendaProductoDetalle])
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
            precio=tp.producto.precio
        )
        for tp in tienda.productos
    ]
