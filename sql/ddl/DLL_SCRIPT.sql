CREATE DATABASE NovaRetail

USE NovaRetail;

/* CREACION DE TABLAS */
CREATE TABLE clientes (
    cliente_id INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    fecha_registro DATE NOT NULL,
    pais VARCHAR(50) NOT NULL
);
---------------
CREATE TABLE productos (
    producto_id INT IDENTITY(1,1) PRIMARY KEY,
    nombre_producto VARCHAR(150) NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    activo BIT NOT NULL
);
---------------
CREATE TABLE ordenes (
    orden_id INT IDENTITY(1,1) PRIMARY KEY,
    cliente_id INT NOT NULL,
    fecha_orden DATETIME NOT NULL,
    estado_orden VARCHAR(50) NOT NULL,
    CONSTRAINT fk_orden_cliente
        FOREIGN KEY (cliente_id)
        REFERENCES clientes(cliente_id)
);
---------------
CREATE TABLE orden_detalle (
    detalle_id INT IDENTITY(1,1) PRIMARY KEY,
    orden_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_detalle_orden
        FOREIGN KEY (orden_id)
        REFERENCES ordenes(orden_id),
    CONSTRAINT fk_detalle_producto
        FOREIGN KEY (producto_id)
        REFERENCES productos(producto_id)
);
---------------
CREATE TABLE orden_detalle (
    detalle_id INT IDENTITY(1,1) PRIMARY KEY,
    orden_id INT NOT NULL,
    producto_id INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    CONSTRAINT fk_detalle_orden
        FOREIGN KEY (orden_id)
        REFERENCES ordenes(orden_id),
    CONSTRAINT fk_detalle_producto
        FOREIGN KEY (producto_id)
        REFERENCES productos(producto_id)
);
---------------
CREATE TABLE pagos (
    pago_id INT IDENTITY(1,1) PRIMARY KEY,
    orden_id INT NOT NULL,
    fecha_pago DATETIME NOT NULL,
    monto_pago DECIMAL(10,2) NOT NULL,
    metodo_pago VARCHAR(50) NOT NULL,
    estado_pago VARCHAR(50) NOT NULL,
    CONSTRAINT fk_pago_orden
        FOREIGN KEY (orden_id)
        REFERENCES ordenes(orden_id)
);
---------------
/*INSERT - DATOS */
-- BULK, ya que nos dieron CSV.

--- Clientes
BULK INSERT clientes
FROM 'C:\Users\Carlo\OneDrive\Escritorio\enterprise-data-lakehouse\data\legacy\clientes.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);

---
BULK INSERT productos
FROM 'C:\Users\Carlo\OneDrive\Escritorio\enterprise-data-lakehouse\data\legacy\productos.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);

----
BULK INSERT ordenes
FROM 'C:\Users\Carlo\OneDrive\Escritorio\enterprise-data-lakehouse\data\legacy\ordenes.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);

---
BULK INSERT orden_detalle
FROM 'C:\Users\Carlo\OneDrive\Escritorio\enterprise-data-lakehouse\data\legacy\orden_detalle.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);

---
BULK INSERT pagos
FROM 'C:\Users\Carlo\OneDrive\Escritorio\enterprise-data-lakehouse\data\legacy\pagos.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    TABLOCK
);


/* Validacion de tablas con la data insertada*/

SELECT COUNT(*) FROM clientes;
SELECT COUNT(*) FROM productos;
SELECT COUNT(*) FROM ordenes;
SELECT COUNT(*) FROM orden_detalle;
SELECT COUNT(*) FROM pagos;


SELECT *
FROM ordenes o
JOIN pagos p ON o.orden_id = p.orden_id
WHERE o.estado_orden <> 'COMPLETADA';


