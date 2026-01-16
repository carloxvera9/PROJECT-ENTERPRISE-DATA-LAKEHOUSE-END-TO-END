import pandas as pd
import os
from pathlib import Path

# ======================================
# PATHS
# ======================================
BRONZE_BASE_PATH = "/opt/airflow/data/bronze/pagos"
SILVER_OUTPUT_PATH = "/opt/airflow/data/silver/pagos"

# ======================================
# 1. OBTENER ÚLTIMA CARGA BRONZE
# ======================================
bronze_path = Path(BRONZE_BASE_PATH)
load_dates = [p for p in bronze_path.iterdir() if p.is_dir()]

if not load_dates:
    raise ValueError("❌ No hay datos en Bronze pagos")

latest_load = max(load_dates, key=lambda p: p.name)
input_file = latest_load / "pagos.parquet"

print(f"📥 Leyendo Bronze desde: {input_file}")

# ======================================
# 2. LECTURA
# ======================================
df = pd.read_parquet(input_file)

# ======================================
# 3. VALIDACIONES CRÍTICAS
# ======================================
required_columns = ["pago_id", "orden_id", "fecha_pago", "monto_pago"]

for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"❌ Columna obligatoria faltante: {col}")

# ======================================
# 4. ELIMINAR DUPLICADOS
# ======================================
df = df.drop_duplicates(subset=["pago_id"])

# ======================================
# 5. MANEJO DE NULOS CRÍTICOS
# ======================================
df = df.dropna(subset=["pago_id", "orden_id"])

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
df["pago_id"] = df["pago_id"].astype(int)
df["orden_id"] = df["orden_id"].astype(int)

df["fecha_pago"] = pd.to_datetime(
    df["fecha_pago"],
    errors="coerce"
)

df["monto_pago"] = pd.to_numeric(
    df["monto_pago"],
    errors="coerce"
)

# ======================================
# 8. ELIMINAR REGISTROS INVÁLIDOS
# ======================================
df = df.dropna(subset=["fecha_pago", "monto_pago"])

# ======================================
# 9. ESCRITURA SILVER
# ======================================
os.makedirs(SILVER_OUTPUT_PATH, exist_ok=True)

output_file = f"{SILVER_OUTPUT_PATH}/pagos_silver.parquet"
df.to_parquet(output_file, index=False)

print(f"✅ SILVER pagos generado en: {output_file}")
