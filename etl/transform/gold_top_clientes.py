import pandas as pd
from datetime import datetime
import os

## Localizamos los datos mas reciente de la capa SILVER

## CLIENTES

SILVER_CLIENTES_BASE_PATH = r"C:\Users\Carlo\OneDrive\Escritorio\enterprise-data-lakehouse\data\silver\clientes"

SILVER_PAGOS_BASE_PATH = r"C:\Users\Carlo\OneDrive\Escritorio\enterprise-data-lakehouse\data\silver\pagos"

SILVER_ORDENES_BASE_PATH = r"C:\Users\Carlo\OneDrive\Escritorio\enterprise-data-lakehouse\data\silver\ordenes"

clientes_load = sorted(os.listdir(SILVER_CLIENTES_BASE_PATH))[-1]
ordenes_load = sorted(os.listdir(SILVER_PAGOS_BASE_PATH))[-1]
pagos_load = sorted(os.listdir(SILVER_ORDENES_BASE_PATH))[-1]

### Leemos los datos de la capa SILVER
df_clientes = pd.read_parquet(f"{SILVER_CLIENTES_BASE_PATH}/{clientes_load}/clientes.parquet")
df_ordenes = pd.read_parquet(f"{SILVER_ORDENES_BASE_PATH}/{ordenes_load}/ordenes.parquet")
df_pagos = pd.read_parquet(f"{SILVER_PAGOS_BASE_PATH}/{pagos_load}/pagos.parquet")

## Unimos las tres tablas para obtener los clientes con compras realizadas

df = (
    df_ordenes[df_ordenes["estado_orden"] == "COMPLETADA"]
    .merge(df_pagos[df_pagos["estado_pago"] == "APROBADO"], on="orden_id")
    .merge(df_clientes, on="cliente_id")
)

## Agregacion por cliente

top_clientes = (
    df.groupby(["cliente_id", "nombre", "apellido"])
      .agg(total_ingresos=("monto_pago", "sum"))
      .reset_index()
      .sort_values("total_ingresos", ascending=False)
      .head(10)
)


## GUARDAR EN GOLD
GOLD_BASE_PATH = r"C:\Users\Carlo\OneDrive\Escritorio\enterprise-data-lakehouse\data\gold\top_clientes"
load_date = datetime.now().strftime("%Y-%m-%d")
output_path = f"{GOLD_BASE_PATH}/load_date={load_date}"
os.makedirs(output_path, exist_ok=True)

top_clientes.to_parquet(
    f"{GOLD_BASE_PATH}/load_date={load_date}/top_clientes_ingresos.parquet",
    index=False
)

##Validacion final
print("Top Clientes en Gold:", top_clientes.shape[0])
print(top_clientes.head())
