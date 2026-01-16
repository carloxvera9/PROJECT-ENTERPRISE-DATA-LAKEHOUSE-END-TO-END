import pandas as pd
import os
from datetime import datetime

# ===============================
# CONFIGURACIÓN
# ===============================
SOURCE_PATH = "/opt/airflow/data/legacy/ordenes.parquet"
BRONZE_BASE_PATH = "/opt/airflow/data/bronze/ordenes"

# ===============================
# LECTURA (DATA CRUDA)
# ===============================
df = pd.read_parquet(SOURCE_PATH)

# ===============================
# VERSIONADO
# ===============================
load_date = datetime.now().strftime("%Y-%m-%d")
output_path = f"{BRONZE_BASE_PATH}/load_date={load_date}"

os.makedirs(output_path, exist_ok=True)

# ===============================
# ESCRITURA BRONZE
# ===============================
output_file = f"{output_path}/ordenes.parquet"
df.to_parquet(output_file, index=False)

print(f"✔ BRONZE ordenes generado en {output_file}")
