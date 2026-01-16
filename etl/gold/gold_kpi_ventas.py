import pandas as pd
import os

# ======================================
# PATHS
# ======================================
ORDENES_PATH = "/opt/airflow/data/silver/ordenes/ordenes_silver.parquet"
PAGOS_PATH = "/opt/airflow/data/silver/pagos/pagos_silver.parquet"
GOLD_PATH = "/opt/airflow/data/gold"

# ======================================
# LECTURA
# ======================================
ordenes = pd.read_parquet(ORDENES_PATH)
pagos = pd.read_parquet(PAGOS_PATH)

# ======================================
# JOIN ÓRDENES + PAGOS
# ======================================
df = ordenes.merge(
    pagos,
    on="orden_id",
    how="inner"
)

# ======================================
# KPIs
# ======================================
total_ventas = df["monto_pago"].sum()
total_pagos = df["pago_id"].nunique()

kpi_ventas = pd.DataFrame([{
    "total_ventas": total_ventas,
    "total_pagos": total_pagos
}])

# ======================================
# ESCRITURA GOLD
# ======================================
os.makedirs(GOLD_PATH, exist_ok=True)

kpi_ventas.to_parquet(
    f"{GOLD_PATH}/kpi_ventas.parquet",
    index=False
)

print("✅ KPI Ventas generado")
print("Total Ventas:", total_ventas)