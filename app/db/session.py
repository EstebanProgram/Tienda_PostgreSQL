from typing import Annotated
from fastapi import Depends
from sqlmodel import Session, create_engine

# Configuracion del motor (PostgreSQL)
# ======================================

# La URL debe coincidir con tu .env, ejemplo:
# postgresql://usuario:password@localhost:5432/mi_db
DATABASE_URL = "postgresql://postgres:tu_password@localhost:5432/tienda_db"

engine = create_engine(DATABASE_URL, echo=True)

# Sesion y dependencia de FastAPI
def get_session():
    """Generador de sesión para dependencias de FastAPI"""
    with Session(engine) as session:
        yield session

SessionDep: Annotated[Session, Depends(get_session)]