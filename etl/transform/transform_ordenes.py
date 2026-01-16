import pandas as pd
import os
from pathlib import Path

# ======================================
# PATHS
# ======================================
BRONZE_BASE_PATH = "/opt/airflow/data/bronze/ordenes"
SILVER_OUTPUT_PATH = "/opt/airflow/data/silver/ordenes"

# ======================================
# 1. OBTENER ÚLTIMA CARGA BRONZE
# ======================================
bronze_path = Path(BRONZE_BASE_PATH)
load_dates = [p for p in bronze_path.iterdir() if p.is_dir()]

if not load_dates:
    raise ValueError("❌ No hay datos en Bronze ordenes")

latest_load = max(load_dates, key=lambda p: p.name)
input_file = latest_load / "ordenes.parquet"

print(f"📥 Leyendo Bronze desde: {input_file}")

# ======================================
# 2. LECTURA
# ======================================
df = pd.read_parquet(input_file)

# ======================================
# 3. VALIDACIONES CRÍTICAS (SOLO CAMPOS REALES)
# ======================================
required_columns = ["orden_id", "cliente_id", "fecha_orden"]

for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"❌ Columna obligatoria faltante: {col}")

# ======================================
# 4. ELIMINAR DUPLICADOS
# ======================================
df = df.drop_duplicates(subset=["orden_id"])

# ======================================
# 5. MANEJO DE NULOS CRÍTICOS
# ======================================
df = df.dropna(subset=["orden_id", "cliente_id"])

# ======================================
# 6. NORMALIZACIÓN DE TEXTOS
# ======================================
for col in df.columns:
    if pd.api.types.is_string_dtype(df[col]):
        df[col] = (
            df[col]
            .fillna("")
            .str.strip()
            .str.upper()
        )

# ======================================
# 7. CONVERSIÓN DE TIPOS
# ======================================
df["orden_id"] = df["orden_id"].astype(int)
df["cliente_id"] = df["cliente_id"].astype(int)

df["fecha_orden"] = pd.to_datetime(
    df["fecha_orden"],
    errors="coerce"
)

# ======================================
# 8. ELIMINAR FECHAS INVÁLIDAS
# ======================================
df = df.dropna(subset=["fecha_orden"])

# ======================================
# 9. ESCRITURA SILVER
# ======================================
os.makedirs(SILVER_OUTPUT_PATH, exist_ok=True)

output_file = f"{SILVER_OUTPUT_PATH}/ordenes_silver.parquet"
df.to_parquet(output_file, index=False)

print(f"✅ SILVER ordenes generado en: {output_file}")
