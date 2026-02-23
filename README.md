# Tienda PostgreSQL

Base de datos relacional de una tienda desarrollada en PostgreSQL.  
El proyecto modela la gestión de clientes, productos y pedidos, aplicando
conceptos de diseño relacional e integridad referencial.

## Descripción

Esta base de datos representa el funcionamiento básico de una tienda online o física,
permitiendo almacenar información sobre:

- Clientes
- Productos
- Pedidos
- Detalles de pedido

El objetivo del proyecto es practicar:

- Diseño de bases de datos
- Creación de tablas (DDL)
- Relaciones y claves foráneas
- Inserción de datos (DML)
- Consultas SQL

## Estructura de la base de datos

Tablas principales:

- **clientes** → información de los clientes
- **productos** → catálogo de productos
- **pedidos** → pedidos realizados
- **detalle_pedidos** → productos incluidos en cada pedido

Relaciones:

- Un cliente puede realizar varios pedidos
- Un pedido puede contener varios productos
- Cada detalle de pedido pertenece a un pedido y a un producto

## Tecnologías utilizadas

- PostgreSQL
- SQL (DDL y DML)
