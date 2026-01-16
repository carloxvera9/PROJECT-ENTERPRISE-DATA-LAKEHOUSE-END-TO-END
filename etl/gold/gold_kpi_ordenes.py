import pandas as pd
import os

ORDENES_PATH = "/opt/airflow/data/silver/ordenes/ordenes_silver.parquet"
GOLD_PATH = "/opt/airflow/data/gold"

ordenes = pd.read_parquet(ORDENES_PATH)

ordenes_por_cliente = (
    ordenes
    .groupby("cliente_id")
    .agg(total_ordenes=("orden_id", "count"))
    .reset_index()
)

ticket_promedio = ordenes_por_cliente["total_ordenes"].mean()

kpi_ordenes = pd.DataFrame([{
    "ordenes_promedio_por_cliente": ticket_promedio
}])

os.makedirs(GOLD_PATH, exist_ok=True)

kpi_ordenes.to_parquet(
    f"{GOLD_PATH}/kpi_ordenes.parquet",
    index=False
)

print("✅ KPI Ordenes generado")
print("Ordenes promedio por cliente:", ticket_promedio)