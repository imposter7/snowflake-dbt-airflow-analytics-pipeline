
from pathlib import Path
import os

import pandas as pd
import snowflake.connector
import yaml
from snowflake.connector.pandas_tools import write_pandas

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "raw"
PROFILE_PATH = Path.home() / ".dbt" / "profiles.yml"

with PROFILE_PATH.open() as file:
    profile = yaml.safe_load(file)["ecommerce_dbt"]["outputs"]["dev"]

password = profile.get("password") or os.getenv("SNOWFLAKE_PASSWORD")
if not password:
    raise RuntimeError("Snowflake password not configured.")

conn = snowflake.connector.connect(
    account=profile["account"],
    user=profile["user"],
    password=password,
    warehouse=profile["warehouse"],
    database=profile["database"],
    schema="RAW",
    role=profile["role"],
)

tables = {
    "CUSTOMERS": "customers.csv",
    "PRODUCTS": "products.csv",
    "ORDERS": "orders.csv",
    "ORDER_ITEMS": "order_items.csv",
}

try:
    for table, filename in tables.items():
        df = pd.read_csv(DATA_DIR / filename)
        df.columns = [column.upper() for column in df.columns]

        # Full refresh makes reruns idempotent for this demo dataset.
        # TRUNCATE commits immediately in Snowflake.
        with conn.cursor() as cursor:
            cursor.execute(f"TRUNCATE TABLE {table}")

        success, chunks, rows, output = write_pandas(
            conn,
            df,
            table_name=table,
            database=profile["database"],
            schema="RAW",
            quote_identifiers=False,
        )

        if not success or rows != len(df):
            raise RuntimeError(f"Load failed for {table}: {output}")

        print(f"Loaded {table}: {rows:,} rows")

    print("\nAll four RAW tables loaded successfully!")

finally:
    conn.close()

