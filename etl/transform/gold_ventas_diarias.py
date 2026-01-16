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

df_ordenes_ok = df_ordenes[df_ordenes['estado_orden'] == 'COMPLETADA']
df_pagos_ok = df_pagos[df_pagos['estado_pago'] == 'APROBADO']

## Unimos ordenes con pagos

df= df_ordenes_ok.merge(
    df_pagos_ok,
    on='orden_id',
    how='inner'
)

## Creamos columna fecha de dia

df['fecha'] = df['fecha_orden'].dt.date

## AGREGACION DE NOGICO

ventas_diarias = ( df.groupby('fecha').agg(
    total_ventas = ('monto_pago', 'sum'),
    numero_ordenes = ('orden_id', 'nunique'),
    ticket_promedio = ('monto_pago', 'mean')
    )
    .reset_index()
)

## Redondeamos las metricas

ventas_diarias['total_ventas'] = ventas_diarias['total_ventas'].round(2)
ventas_diarias['ticket_promedio'] = ventas_diarias['ticket_promedio'].round(2)


########################### GUARDAMOS LA DATA TRANSFORMADA EN LA CAPA GOLD ######################################

GOLD_BASE_PATH = r"C:\Users\Carlo\OneDrive\Escritorio\enterprise-data-lakehouse\data\gold\ventas_diarias"
load_date = datetime.now().strftime("%Y-%m-%d")
output_path = f"{GOLD_BASE_PATH}/load_date={load_date}"
os.makedirs(output_path, exist_ok=True)
ventas_diarias.to_parquet(f"{output_path}/ventas_diarias.parquet", index=False)
##Validacion final
print("Días con ventas en Gold:", ventas_diarias.shape[0])
print(ventas_diarias.head())
