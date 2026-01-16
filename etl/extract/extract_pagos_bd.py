##instalamos el paquete pyodbc si no lo tenemos 
##python -m pip install pyodbc
##python -m pip install pandas
##python -m pip install pyarrow #para guardar en formato parquet
import pyodbc  ##Me comunico con bases de datos SQL Server
import pandas as pd ##para manimular dataframes
from datetime import datetime ##MANEJAR FECHAS
import os ##MANEJAR RUTAS DE ARCHIVOS

## Realizaremos carga incremental basada en fecha de última carga
LAST_LOAD_DATE = "2023-01-01"

## Configuración de conexión a la base de datos SQL Server
conn = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=NovaRetail;"
    "UID=sa;"
    "PWD=sql;"
)

## Consulta SQL para extraer datos de pagos modificados después de LAST_LOAD_DATE
query = f"""
SELECT
    pago_id,
    orden_id,
    fecha_pago,
    monto_pago,
    metodo_pago,
    estado_pago
FROM pagos
WHERE fecha_pago > '{LAST_LOAD_DATE}'

"""

## Ya tengo los datos en un dataframe de pandas
df_pagos = pd.read_sql(query, conn)


## Preparamos la data para la capa bronze 
load_date = datetime.now().strftime("%Y-%m-%d")
output_path =rf"C:\Users\Carlo\OneDrive\Escritorio\enterprise-data-lakehouse\data\bronze\pagos\load_date={load_date}"
os.makedirs(output_path, exist_ok=True) 

## Guardamos el dataframe como parquet en la ruta de la capa bronze
df_pagos.to_parquet(
    f"{output_path}/pagos.parquet",
    index=False
)

print(f"Extracción completada. {len(df_pagos)} registros extraídos y guardados en {output_path}.")
print("Órdenes extraídas:", df_pagos.shape[0])
print(df_pagos.head())