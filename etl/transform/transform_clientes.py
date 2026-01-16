import pandas as pd
import os
from pathlib import Path

# ======================================
# PATHS
# ======================================
BRONZE_BASE_PATH = "/opt/airflow/data/bronze/clientes"
SILVER_OUTPUT_PATH = "/opt/airflow/data/silver/clientes"

# ======================================
# 1. OBTENER LA ÚLTIMA CARGA DE BRONZE
# ======================================
bronze_path = Path(BRONZE_BASE_PATH)

load_dates = [p for p in bronze_path.iterdir() if p.is_dir()]

if not load_dates:
    raise ValueError("❌ No hay datos en Bronze clientes")

latest_load = max(load_dates, key=lambda p: p.name)

input_file = latest_load / "clientes.parquet"

print(f"📥 Leyendo Bronze desde: {input_file}")

# ======================================
# 2. LECTURA
# ======================================
df = pd.read_parquet(input_file)

# ======================================
# 3. VALIDACIONES BÁSICAS
# ======================================
required_columns = ["cliente_id"]

for col in required_columns:
    if col not in df.columns:
        raise ValueError(f"❌ Columna obligatoria faltante: {col}")

# ======================================
# 4. ELIMINAR DUPLICADOS
# ======================================
df = df.drop_duplicates(subset=["cliente_id"])

# ======================================
# 5. MANEJO DE NULOS CRÍTICOS
# ======================================
df = df.dropna(subset=["cliente_id"])

# ======================================
# 6. NORMALIZACIÓN DE TEXTOS (SEGURO)
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
# 7. ASEGURAR TIPOS
# ======================================
df["cliente_id"] = df["cliente_id"].astype(int)

# ======================================
# 8. ESCRITURA SILVER
# ======================================
os.makedirs(SILVER_OUTPUT_PATH, exist_ok=True)

output_file = f"{SILVER_OUTPUT_PATH}/clientes_silver.parquet"

df.to_parquet(output_file, index=False)

print(f"✅ SILVER clientes generado en: {output_file}")
print("Registros transformados:", df.shape[0])