import pandas as pd
from datetime import datetime
import os

## Localizamos los datos mas reciente de la capa SILVER

## PAGOS

SILVER_PAGOS_BASE_PATH = r"C:\Users\Carlo\OneDrive\Escritorio\enterprise-data-lakehouse\data\silver\pagos"

pagos_load_dates = sorted(os.listdir(SILVER_PAGOS_BASE_PATH))

lasted_pagos_load = pagos_load_dates[-1]

df_pagos = pd.read_parquet(f"{SILVER_PAGOS_BASE_PATH}/{lasted_pagos_load}/pagos.parquet")


## Filtro pagos validos

df = df_pagos[df_pagos["estado_pago"] == "APROBADO"]

## Agregacion por metodo de pago

ingresos_metodo = (
    df.groupby("metodo_pago")
      .agg(
          total_ingresos=("monto_pago", "sum"),
          cantidad_pagos=("pago_id", "count")
      )
      .reset_index()
)

## GUARDAR EN GOLD
GOLD_BASE_PATH = r"C:\Users\Carlo\OneDrive\Escritorio\enterprise-data-lakehouse\data\gold\ingresos_metodo_pago"
load_date = datetime.now().strftime("%Y-%m-%d")
output_path = f"{GOLD_BASE_PATH}/load_date={load_date}"
os.makedirs(output_path, exist_ok=True)
ingresos_metodo.to_parquet(f"{output_path}/ingresos_metodo_pago.parquet", index=False)

##Validacion final
print("Ingresos por Metodo de Pago en Gold:", ingresos_metodo.shape[0])
print(ingresos_metodo.head())

