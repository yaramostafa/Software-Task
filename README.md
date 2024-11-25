# Data Processing Pipeline with Dynamic Expression Parsing

This repository contains a Python implementation for processing and transforming data records based on configurable arithmetic and regex-based equations. It uses a custom Lexer, Parser, and Interpreter to evaluate mathematical and logical expressions dynamically.

---

## Overview

This project processes data records (data.txt) in real-time by:
- Parsing and interpreting equations provided in a configuration file (config.txt).
  example :
  ATTR+50*(ATTR/10)
  Regex(ATTR, "^dog")
- Performing computations or regex-based matching on incoming data.
- Storing processed results in a SQLite database (processed_data.db).
- Managing KPIs and their associations with assets using a Django-based web interface.

---

## Architecture of calc1.py

1. **Lexer**: Converts input strings (equations) into tokens.
2. **Parser**: Constructs an Abstract Syntax Tree (AST) from tokens.
3. **Interpreter**: Traverses the AST to evaluate expressions.
4. **FileReader**: Reads new data records incrementally from a file.
5. **DataProcessor**: Processes records using the provided equation.
6. **SQLiteDataSink**: Stores the processed output into a SQLite database.

---

## Django Task

The Django application provides APIs for managing KPIs and linking them to assets_id. 

### Tasks Implemented:
1. **KPI App**:
   - Created a `KPI` app in Django to manage KPI information and their linkage to assets.
   
2. **Models**:
   - `KPI`: Stores KPI details such as name, expression, and optional description.
   - `AssetKPI`: Links KPIs to asset IDs fetched dynamically from the SQLite database.

3. **Endpoints**:
   - **List/Create KPI**: `/api/kpi/` (supports GET and POST methods).
   - **Link Asset to KPI**: `/api/kpi/link_asset/` (supports POST to create associations).

4. **Swagger Documentation**:
   - Interactive API documentation available at `/swagger/`.
   - ReDoc UI available at `/redoc/`.
   - Swagger JSON schema available at `/swagger.json`.

---

## Django Code Details

### `models.py`
Defines two models:
- **KPI**: Represents the KPI with fields `name`, `expression`, and an optional `description`.
- **AssetKPI**: Links KPIs to assets using a foreign key relationship, with asset IDs dynamically fetched from the SQLite database.

### `urls.py`
Defines API routes:
- **`admin/`**: Django admin panel.
- **`api/kpi/kpis/`**: Endpoint to list or create KPIs using the `KPIListCreateView`. (Supports GET and POST).
- **`api/kpi/assets/link/`**: Endpoint to link assets to KPIs using the `AssetKPICreateView`. (Supports POST).
- **`api/kpi/`**: Defaults to the `KPIListCreateView` for listing or creating KPIs. (Supports GET and POST).
- **`swagger/`**: Interactive Swagger UI for API documentation.
- **`redoc/`**: ReDoc UI for a detailed API overview.
- **`swagger.json`**: Provides the raw Swagger JSON schema.
---
