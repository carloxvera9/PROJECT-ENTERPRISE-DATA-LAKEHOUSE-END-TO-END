# 🚀 NovaRetail — Plataforma End-to-End de Ingeniería de Datos y BI

## 📌 Descripción general del proyecto

**NovaRetail** es un proyecto **end-to-end de Ingeniería de Datos y Business Intelligence**, diseñado para simular cómo una **empresa de Retail & E-commerce** implementa una **plataforma moderna de datos tipo Lakehouse**, desde la extracción de datos legacy hasta la visualización ejecutiva.

Este proyecto fue desarrollado con un **enfoque de portafolio profesional**, priorizando:

- Arquitectura **Lakehouse (Bronze / Silver / Gold)**
- Pipelines **ETL en Python**
- **Orquestación con Apache Airflow (Docker)**
- Consumo analítico con **Power BI**
- Ejecución **local y sin costos**
- Código entendible, documentado y explicable

🎯 **Objetivo principal:** demostrar competencias reales para roles de**Data Engineer / Analytics Engineer / BI Analyst**.

## 🏢 Contexto de negocio (caso realista)

### Rubro

**Retail & E-commerce con operaciones financieras**

Este rubro se elige estratégicamente porque:

- Es muy común en entrevistas técnicas
- Combina datos transaccionales y analíticos
- Permite KPIs financieros, de clientes y pagos
- Escala fácilmente a escenarios enterprise

### Empresa simulada — _NovaRetail_

Grupo regional con:

- Clientes en múltiples países
- Órdenes de venta
- Procesamiento de pagos
- Reglas de negocio y regulatorias por país

## 🎯 Objetivos de negocio

- Centralizar datos de múltiples sistemas
- Mejorar la calidad y trazabilidad de la información
- Obtener KPIs claros para toma de decisiones
- Analizar ventas, clientes y pagos por país
- Reducir procesos manuales de reporte

## 🧠 Objetivos técnicos (Ingeniería de Datos)

- Diseñar una arquitectura **Lakehouse (Bronze / Silver / Gold)**
- Construir pipelines **ETL reproducibles**
- Orquestar procesos con **Apache Airflow**
- Aplicar buenas prácticas de:
  - particionado
  - separación por capas
  - reglas de negocio

- Entregar datos listos para **Business Intelligence**

## 🏗️ Arquitectura general

Fuentes Legacy / CSV simulados

↓

ETL en Python (Extract / Transform)

↓

Data Lake Local (Parquet)

Bronze → Silver → Gold

↓

Orquestación

Apache Airflow (Docker)

↓

Capa de Consumo

Power BI

## 🧱 Fases del proyecto

### 🟤 Capa Bronze — Ingesta

**Objetivo:** almacenar datos crudos sin modificar

- Extracción desde fuentes legacy simuladas
- Almacenamiento en formato **Parquet**
- Particionado por fecha de carga

### ⚪ Capa Silver — Limpieza y conformado

**Objetivo:** datos limpios y confiables

Transformaciones aplicadas:

- Normalización de textos
- Validación de tipos
- Limpieza de nulos
- Relaciones entre entidades
- Reglas de negocio

### 🟡 Capa Gold — Métricas de negocio

**Objetivo:** datos listos para análisis y BI

KPIs generados:

- Ventas totales
- Pagos totales
- Clientes activos
- Ticket promedio
- Métodos de pago

Incluye reglas reales, por ejemplo:

> **YAPE y PLIN solo son válidos para Perú**, y no se contabilizan en otros países.

### 🔄 Orquestación

**Objetivo:** automatizar el flujo completo

- DAGs en Apache Airflow
- Dependencias claras
- Reintentos y control de fallos
- Ejecución reproducible con Docker

### 📊 Business Intelligence

**Objetivo:** visualización ejecutiva

Dashboard en **Power BI** con:

- KPIs financieros
- Clientes por país (mapa)
- Métodos de pago
- Análisis temporal
- Indicadores regulatorios

## 📊 Dashboard Ejecutivo (Power BI)

El dashboard está orientado a **gerencia y directores**, mostrando:

- Estado general del negocio
- Distribución geográfica de clientes
- Preferencias de pago por país
- KPIs claros y accionables

✔ Visual limpio✔ Enfoque ejecutivo✔ Métricas entendibles

## 📂 Estructura del repositorio

novaretail-end-to-end-data-platform/

│

├── data/

│ ├── bronze/

│ ├── silver/

│ └── gold/

│

├── etl/

│ ├── extract/

│ └── transform/

│

├── orchestration/

│ └── airflow/

│

├── powerbi/

│ └── novaretail_dashboard.pbix

│

├── docs/

│

└── README.md

## 🛠️ Tecnologías utilizadas

- Python 3.12
- Pandas
- Parquet
- Apache Airflow
- Docker
- Power BI
- Git & GitHub

## 💰 Estrategia de costos

- Ejecución completamente local
- Docker para aislamiento de entornos
- Sin uso de servicios pagos
- Datasets pequeños pero realistas

## 👤 Autor

**Carlos Alexandro Vera Torres**📍 Perú 🇵🇪
