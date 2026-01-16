import pandas as pd
import os

CLIENTES_PATH = "/opt/airflow/data/silver/clientes/clientes_silver.parquet"
ORDENES_PATH = "/opt/airflow/data/silver/ordenes/ordenes_silver.parquet"
GOLD_PATH = "/opt/airflow/data/gold"

clientes = pd.read_parquet(CLIENTES_PATH)
ordenes = pd.read_parquet(ORDENES_PATH)

clientes_activos = ordenes["cliente_id"].nunique()
total_clientes = clientes["cliente_id"].nunique()

kpi_clientes = pd.DataFrame([{
    "total_clientes": total_clientes,
    "clientes_activos": clientes_activos
}])

os.makedirs(GOLD_PATH, exist_ok=True)

kpi_clientes.to_parquet(
    f"{GOLD_PATH}/kpi_clientes.parquet",
    index=False
)

print("✅ KPI Clientes generado")
print("Total Clientes:", total_clientes)
