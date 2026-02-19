from fastapi import APIRouter, HTTPException
from sqlmodel import select
from db.session import SessionDep
from models.tables import Tienda, TiendaProducto
from models.schemas import TiendaPublic, TiendaUpdate, TiendaProductoDetalle, TiendaProductoUpdate, TiendaProductoBase

router = APIRouter(prefix="/tiendas", tags=["tiendas"])

# Crear tienda
@router.post("/", response_model=TiendaPublic)
def create_tienda(tienda: TiendaPublic, session: SessionDep):
    db_tienda = Tienda.model_validate(tienda)
    session.add(db_tienda)
    session.commit()
    session.refresh(db_tienda)
    return db_tienda

# Leer todas las tiendas
@router.get("/", response_model=list[TiendaPublic])
def read_tiendas(session: SessionDep):
    return session.exec(select(Tienda)).all()

# Leer por ID
@router.get("/{tienda_id}", response_model=TiendaPublic)
def read_tienda(tienda_id: int, session: SessionDep):
    tienda = session.get(Tienda, tienda_id)
    if not tienda:
        raise HTTPException(404, "Tienda no encontrada")
    return tienda

# Leer por nombre (like)
@router.get("/nombre/", response_model=list[TiendaPublic])
def read_tienda_por_nombre(nombre: str, session: SessionDep):
    tiendas = session.exec(select(Tienda).where(Tienda.nombre.ilike(f"%{nombre}%"))).all()
    if not tiendas:
        raise HTTPException(404, "No se encontraron tiendas con ese nombre")
    return tiendas

# Actualizar
@router.patch("/{tienda_id}", response_model=TiendaPublic)
def update_tienda(tienda_id: int, tienda: TiendaUpdate, session: SessionDep):
    tienda_db = session.get(Tienda, tienda_id)
    if not tienda_db:
        raise HTTPException(404, "Tienda no encontrada")
    data = tienda.model_dump(exclude_unset=True)
    tienda_db.sqlmodel_update(data)
    session.commit()
    session.refresh(tienda_db)
    return tienda_db

# Eliminar
@router.delete("/{tienda_id}")
def delete_tienda(tienda_id: int, session: SessionDep):
    tienda = session.get(Tienda, tienda_id)
    if not tienda:
        raise HTTPException(404, "Tienda no encontrada")
    session.delete(tienda)
    session.commit()
    return {"ok": True}
