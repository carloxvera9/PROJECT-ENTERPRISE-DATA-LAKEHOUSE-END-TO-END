from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime, timedelta

default_args = {
    "owner": "carlos",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="novaretail_etl_pipeline",
    default_args=default_args,
    description="ETL Lakehouse Retail - Bronze Silver Gold",
    schedule_interval=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["retail", "lakehouse", "etl"],
) as dag:

    # ===============================
    # EXTRAER DATA LEGACY (BRONZE)
    # ===============================
    with TaskGroup(group_id="extract_legacy", tooltip="Extraer data legacy a Bronze") as extract_legacy:

        extract_clientes = BashOperator(
            task_id="extract_clientes",
            bash_command="python /opt/airflow/etl/extract/extract_clientes.py",
        )

        extract_ordenes = BashOperator(
            task_id="extract_ordenes",
            bash_command="python /opt/airflow/etl/extract/extract_ordenes.py",
        )

        extract_pagos = BashOperator(
            task_id="extract_pagos",
            bash_command="python /opt/airflow/etl/extract/extract_pagos.py",
        )

    # ===============================
    # SILVER - LIMPIEZA / VALIDACIÓN
    # ===============================
    with TaskGroup(group_id="silver_transform", tooltip="Transformaciones Silver") as silver_transform:

        transform_clientes = BashOperator(
            task_id="transform_clientes",
            bash_command="python /opt/airflow/etl/transform/transform_clientes.py",
        )

        transform_ordenes = BashOperator(
            task_id="transform_ordenes",
            bash_command="python /opt/airflow/etl/transform/transform_ordenes.py",
        )

        transform_pagos = BashOperator(
            task_id="transform_pagos",
            bash_command="python /opt/airflow/etl/transform/transform_pagos.py",
        )

    # ===============================
    # GOLD - KPIs / CONSUMO
    # ===============================
    with TaskGroup(group_id="gold_kpis", tooltip="KPIs Gold para negocio") as gold_kpis:

        gold_kpi_ventas = BashOperator(
            task_id="gold_kpi_ventas",
            bash_command="python /opt/airflow/etl/gold/gold_kpi_ventas.py",
        )

        gold_kpi_clientes = BashOperator(
            task_id="gold_kpi_clientes",
            bash_command="python /opt/airflow/etl/gold/gold_kpi_clientes.py",
        )

        gold_kpi_ordenes = BashOperator(
            task_id="gold_kpi_ordenes",
            bash_command="python /opt/airflow/etl/gold/gold_kpi_ordenes.py",
        )

    # ===============================
    # DEPENDENCIAS ENTRE CAPAS
    # ===============================
    extract_legacy >> silver_transform >> gold_kpis
