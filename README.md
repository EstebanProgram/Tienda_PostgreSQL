# Tienda API - FastAPI + SQLModel + PostgreSQL

Este proyecto es una API de ejemplo para gestionar proveedores, tiendas y productos usando FastAPI y SQLModel, con PostgreSQL como base de datos. Permite crear, leer, actualizar y eliminar registros, además de gestionar stock y buscar por nombre.

## Requisitos

- Python >= 3.11
- PostgreSQL
- pip

## Instalación

Clona el repositorio y entra en el directorio del proyecto. Crea y activa un entorno virtual. Instala las dependencias desde `requirements.txt`. Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

POSTGRES_USER=postgres
POSTGRES_PASSWORD=tu_password
POSTGRES_DB=tienda_db
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DEBUG=True


Cambia `tu_password` por la contraseña que hayas configurado en PostgreSQL. `DEBUG=True` activa recarga automática y logs para desarrollo.

## Configuración de la base de datos

Asegúrate de que PostgreSQL está corriendo. Crea la base de datos si no existe: `CREATE DATABASE tienda_db;`. Crea el usuario y asigna contraseña si es necesario: `CREATE USER postgres WITH PASSWORD 'tu_password'; GRANT ALL PRIVILEGES ON DATABASE tienda_db TO postgres;`. Esto solo es necesario si el usuario/postgres no existía previamente.

## Ejecución de la API

Arranca el servidor en desarrollo con `uvicorn app.main:app --reload`. Esto levantará la API en `http://127.0.0.1:8000`. La documentación automática de FastAPI estará disponible en Swagger UI (`/docs`) y ReDoc (`/redoc`).

## Endpoints principales

- `/proveedores/` → CRUD de proveedores  
- `/tiendas/` → CRUD de tiendas  
- `/productos/` → CRUD de productos  
- `/tiendas/{tienda_id}/productos/` → Gestionar stock de productos por tienda  
- `/tiendas/nombre/?nombre=<nombre>` → Buscar tiendas por nombre (LIKE)  
- `/productos/nombre/?nombre=<nombre>` → Buscar productos por nombre (LIKE)  
- `/proveedores/nombre/?nombre=<nombre>` → Buscar proveedores por nombre (LIKE)  

## Notas y recomendaciones

Todos los modelos usan **ORM** (SQLModel) para relaciones, cascadas y consultas más limpias. Se recomienda **PostgreSQL** para aprovechar funcionalidades avanzadas como **JSONB**, índices y consultas más complejas. Los endpoints de búsqueda usan `ilike` para no distinguir mayúsculas y minúsculas. Se usa `Session` de SQLModel para manejo de transacciones (`commit`, `refresh`, consultas ORM). No olvides añadir `.env` a `.gitignore` si vas a subir el proyecto a GitHub. Para desarrollo rápido puedes usar `DEBUG=True`; en producción conviene desactivarlo.

## Ejemplo de uso

Crear un proveedor: `POST /proveedores/` con `{"nombre": "Proveedor1", "contacto": "contacto@correo.com"}`.
Crear una tienda: `POST /tiendas/` con `{"nombre": "Tienda Central", "direccion": "Calle Falsa 123"}`. 
Crear un producto: `POST /productos/` con `{"nombre": "Producto A", "precio": 12.50, "id_proveedor": 1}`. 
Añadir un producto a la tienda: `POST /tiendas/1/productos/1` con `{"stock": 100}`. 
Buscar productos con stock mínimo: `GET /tiendas/1/productos/stock?min_stock=50`. 
Buscar tiendas por nombre parcial: `GET /tiendas/nombre/?nombre=Central`.