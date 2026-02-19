from fastapi import APIRouter, HTTPException
from sqlmodel import select
from db.session import SessionDep
from models.tables import Proveedor
from models.schemas import ProveedorPublic, ProveedorUpdate

router = APIRouter(prefix="/proveedores", tags=["proveedores"])

# Crear proveedor
@router.post("/", response_model=ProveedorPublic)
def create_proveedor(proveedor: ProveedorPublic, session: SessionDep):
    db_proveedor = Proveedor.model_validate(proveedor)
    session.add(db_proveedor)
    session.commit()
    session.refresh(db_proveedor)
    return db_proveedor

# Leer todos los proveedores
@router.get("/", response_model=list[ProveedorPublic])
def read_proveedores(session: SessionDep):
    return session.exec(select(Proveedor)).all()

# Leer por ID
@router.get("/{proveedor_id}", response_model=ProveedorPublic)
def read_proveedor(proveedor_id: int, session: SessionDep):
    proveedor = session.get(Proveedor, proveedor_id)
    if not proveedor:
        raise HTTPException(404, "Proveedor no encontrado")
    return proveedor

# Leer por nombre (like)
@router.get("/nombre/", response_model=list[ProveedorPublic])
def read_proveedor_por_nombre(nombre: str, session: SessionDep):
    proveedores = session.exec(select(Proveedor).where(Proveedor.nombre.ilike(f"%{nombre}%"))).all()
    if not proveedores:
        raise HTTPException(404, "No se encontraron proveedores con ese nombre")
    return proveedores

# Actualizar
@router.patch("/{proveedor_id}", response_model=ProveedorPublic)
def update_proveedor(proveedor_id: int, proveedor: ProveedorUpdate, session: SessionDep):
    proveedor_db = session.get(Proveedor, proveedor_id)
    if not proveedor_db:
        raise HTTPException(404, "Proveedor no encontrado")
    data = proveedor.model_dump(exclude_unset=True)
    proveedor_db.sqlmodel_update(data)
    session.commit()
    session.refresh(proveedor_db)
    return proveedor_db

# Eliminar
@router.delete("/{proveedor_id}")
def delete_proveedor(proveedor_id: int, session: SessionDep):
    proveedor = session.get(Proveedor, proveedor_id)
    if not proveedor:
        raise HTTPException(404, "Proveedor no encontrado")
    session.delete(proveedor)
    session.commit()
    return {"ok": True}
