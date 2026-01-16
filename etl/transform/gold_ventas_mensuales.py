import pandas as pd
from datetime import datetime
import os

## Localizamos los datos mas reciente de la capa SILVER

## ORDENES
SILVER_ORDENES_BASE_PATH = r"C:\Users\Carlo\OneDrive\Escritorio\enterprise-data-lakehouse\data\silver\ordenes"

ordenes_load_dates =  sorted(os.listdir(SILVER_ORDENES_BASE_PATH))

lasted_ordenes_load = ordenes_load_dates[-1]

df_ordenes = pd.read_parquet(f"{SILVER_ORDENES_BASE_PATH}/{lasted_ordenes_load}/ordenes.parquet")


## PAGOS

SILVER_PAGOS_BASE_PATH = r"C:\Users\Carlo\OneDrive\Escritorio\enterprise-data-lakehouse\data\silver\pagos"

pagos_load_dates = sorted(os.listdir(SILVER_PAGOS_BASE_PATH))

lasted_pagos_load = pagos_load_dates[-1]

df_pagos = pd.read_parquet(f"{SILVER_PAGOS_BASE_PATH}/{lasted_pagos_load}/pagos.parquet")


#### FILTRAR SOLO VENTAS VALIDAS

df = df_ordenes[df_ordenes["estado_orden"] == "COMPLETADA"].merge(
    df_pagos[df_pagos["estado_pago"] == "APROBADO"],
    on="orden_id",
    how="inner"
)

#### CREAR COLUMNAS AÑO Y MES 

df["anio_mes"] = df["fecha_orden"].dt.to_period("M").astype(str)

## AGREGACION MENSUAL

ventas_mensuales = (
    df.groupby("anio_mes")
      .agg(
          total_ventas=("monto_pago", "sum"),
          cantidad_ordenes=("orden_id", "nunique")
      )
      .reset_index()
)


## GUARDAR EN GOLD

GOLD_BASE_PATH = r"C:\Users\Carlo\OneDrive\Escritorio\enterprise-data-lakehouse\data\gold\ventas_mensuales"
load_date = datetime.now().strftime("%Y-%m-%d")
output_path = f"{GOLD_BASE_PATH}/load_date={load_date}"
os.makedirs(output_path, exist_ok=True)

ventas_mensuales.to_parquet(f"{output_path}/ventas_diarias.parquet", index=False)
##Validacion final
print("Días con ventas en Gold:", ventas_mensuales.shape[0])
print(ventas_mensuales.head())

