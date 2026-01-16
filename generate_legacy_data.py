from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta
import os

fake = Faker("es_MX")
random.seed(42)

BASE_PATH = "data/legacy"
os.makedirs(BASE_PATH, exist_ok=True)

# Volúmenes
N_CLIENTES = 5000
N_PRODUCTOS = 500
N_ORDENES = 8000

# ------------------------
# CLIENTES
# ------------------------
clientes = []
for i in range(1, N_CLIENTES + 1):
    clientes.append({
        "cliente_id": i,
        "nombre": fake.first_name(),
        "apellido": fake.last_name(),
        "email": fake.email(),
        "fecha_registro": fake.date_between(start_date="-3y", end_date="-30d"),
        "pais": random.choice(["Perú", "Chile", "Colombia", "México", "Argentina"])
    })

df_clientes = pd.DataFrame(clientes)
df_clientes.to_csv(f"{BASE_PATH}/clientes.csv", index=False)

# ------------------------
# PRODUCTOS
# ------------------------
categorias = ["Tecnología", "Hogar", "Moda", "Deportes", "Salud", "Alimentos"]

productos = []
for i in range(1, N_PRODUCTOS + 1):
    productos.append({
        "producto_id": i,
        "nombre_producto": f"{fake.word().capitalize()} {fake.word().capitalize()}",
        "categoria": random.choice(categorias),
        "precio_unitario": round(random.uniform(50, 4500), 2),
        "activo": 1 if random.random() < 0.95 else 0
    })

df_productos = pd.DataFrame(productos)
df_productos.to_csv(f"{BASE_PATH}/productos.csv", index=False)

# ------------------------
# ORDENES
# ------------------------
ordenes = []
for i in range(1, N_ORDENES + 1):
    ordenes.append({
        "orden_id": i,
        "cliente_id": random.randint(1, N_CLIENTES),
        "fecha_orden": fake.date_time_between(start_date="-1y", end_date="now"),
        "estado_orden": random.choices(
            ["COMPLETADA", "PENDIENTE", "CANCELADA"],
            weights=[0.65, 0.2, 0.15]
        )[0]
    })

df_ordenes = pd.DataFrame(ordenes)
df_ordenes.to_csv(f"{BASE_PATH}/ordenes.csv", index=False)

# ------------------------
# ORDEN DETALLE
# ------------------------
detalle = []
detalle_id = 1

for _, orden in df_ordenes.iterrows():
    n_items = random.randint(1, 4)
    productos_sample = random.sample(productos, n_items)

    for prod in productos_sample:
        detalle.append({
            "detalle_id": detalle_id,
            "orden_id": orden["orden_id"],
            "producto_id": prod["producto_id"],
            "cantidad": random.randint(1, 3),
            "precio_unitario": prod["precio_unitario"]
        })
        detalle_id += 1

df_detalle = pd.DataFrame(detalle)
df_detalle.to_csv(f"{BASE_PATH}/orden_detalle.csv", index=False)

# ------------------------
# PAGOS (solo completadas)
# ------------------------
pagos = []
pago_id = 1

for orden_id in df_ordenes[df_ordenes["estado_orden"] == "COMPLETADA"]["orden_id"]:
    od = df_detalle[df_detalle["orden_id"] == orden_id]
    monto = round((od["cantidad"] * od["precio_unitario"]).sum(), 2)

    pagos.append({
        "pago_id": pago_id,
        "orden_id": orden_id,
        "fecha_pago": fake.date_time_between(start_date="-1y", end_date="now"),
        "monto_pago": monto,
        "metodo_pago": random.choice(["TARJETA", "YAPE", "PLIN", "TRANSFERENCIA"]),
        "estado_pago": "APROBADO"
    })
    pago_id += 1

df_pagos = pd.DataFrame(pagos)
df_pagos.to_csv(f"{BASE_PATH}/pagos.csv", index=False)

print("✔ CSV legacy generados correctamente")
