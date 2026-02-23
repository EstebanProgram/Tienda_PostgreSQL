# Tienda API

API REST para gestionar proveedores, tiendas, productos y stock, construida con FastAPI, SQLModel y PostgreSQL.

## Tabla de Contenidos

- [Tecnologías](#tecnologías)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Ejecutar el proyecto](#ejecutar-el-proyecto)
- [Endpoints disponibles](#endpoints-disponibles)
- [Notas y recomendaciones](#notas-y-recomendaciones)

---

## Tecnologías

- Python 3.11+
- FastAPI
- SQLModel (ORM sobre SQLAlchemy)
- PostgreSQL
- Pydantic (para validación de datos)
- Uvicorn (servidor ASGI)

---

## Estructura del proyecto
tienda_app/
│
├── app/
│ ├── main.py # Entry point de FastAPI con todos los endpoints
│ ├── config.py # Configuración de entorno (.env)
│ ├── models/ # Modelos y schemas
│ │ ├── init.py
│ │ ├── base.py # Clases base para herencia
│ │ ├── tables.py # Tablas ORM: Proveedor, Tienda, Producto, TiendaProducto
│ │ └── schemas.py # Schemas Pydantic para requests/responses
│ ├── db/ # Conexión y setup de base de datos
│ │ ├── init.py
│ │ ├── session.py # Engine y Session
│ │ └── init_db.py # Crear tablas
│ ├── routers/ # Endpoints separados por recurso
│ │ ├── init.py
│ │ ├── proveedores.py
│ │ ├── tiendas.py
│ │ └── productos.py
│ └── utils/
│ └── helpers.py
│
├── .env # Variables de entorno (no subir a GitHub)
├── requirements.txt
└── README.md

---

## Instalación

Clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd tienda_app
```

Crear y activar el entorno virtual:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Configuración
Crea un archivo .env en la raíz con las siguientes variables:
```env
POSTGRES_USER=tu_usuario
POSTGRES_PASSWORD=tu_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=tienda_db
DEBUG=True
```

Recuerda cambiar tu usuario y password

## Endpoints disponibles

### Proveedores
- `POST /proveedores/` – Crear proveedor
- `GET /proveedores/` – Listar proveedores
- `GET /proveedores/{id}` – Obtener proveedor por ID
- `GET /proveedores/nombre/` – Buscar por nombre
- `PATCH /proveedores/{id}` – Actualizar proveedor
- `DELETE /proveedores/{id}` – Eliminar proveedor

### Tiendas
- `POST /tiendas/` – Crear tienda
- `GET /tiendas/` – Listar tiendas
- `GET /tiendas/{id}` – Obtener tienda por ID
- `GET /tiendas/nombre/` – Buscar por nombre
- `PATCH /tiendas/{id}` – Actualizar tienda
- `DELETE /tiendas/{id}` – Eliminar tienda

### Productos
- `POST /productos/` – Crear producto
- `GET /productos/` – Listar productos
- `GET /productos/{id}` – Obtener producto por ID
- `GET /productos/nombre/` – Buscar por nombre
- `PATCH /productos/{id}` – Actualizar producto
- `DELETE /productos/{id}` – Eliminar producto

### Stock Tienda-Producto
- `POST /tiendas/{tienda_id}/productos/{producto_id}` – Añadir producto a tienda
- `GET /tiendas/{tienda_id}/productos` – Listar productos de una tienda
- `PATCH /tiendas/{tienda_id}/productos/{producto_id}` – Actualizar stock
- `DELETE /tiendas/{tienda_id}/productos/{producto_id}` – Eliminar producto de tienda
