import os

import snowflake.connector
from assets_smoke_test import python_and_dbt_assets
from assets_smoke_test.python_and_dbt_assets import (
    DBT_PROFILES_DIR,
    DBT_PROJECT_DIR,
    raw_country_populations,
)
from dagster import load_assets_from_modules, materialize
from dagster_dbt import DbtCliClientResource
from dagster_snowflake_pandas import SnowflakePandasIOManager


def smoke_all_test():
    snowflake_config = {
        "user": os.environ["SNOWFLAKE_USER"],
        "password": os.environ["SNOWFLAKE_PASSWORD"],
        "account": os.environ["SNOWFLAKE_ACCOUNT"],
        "database": os.environ["SNOWFLAKE_DATABASE"],
    }

    io_manager = SnowflakePandasIOManager(**snowflake_config)

    dbt_resource = DbtCliClientResource(
        target="smoke_test", project_dir=DBT_PROJECT_DIR, profiles_dir=DBT_PROFILES_DIR
    )

    source_assets = [raw_country_populations]

    conn = snowflake.connector.connect(**snowflake_config)

    for source_asset in source_assets:
        db_name = snowflake_config["database"]
        table_name = f"{db_name}.public.{source_asset.key.path[-1]}"
        columns_str = ", ".join(
            [
                f"{column.name} {column.type}"
                for column in source_asset.metadata["column_schema"].schema.columns
            ]
        )
        conn.cursor().execute(f"CREATE OR REPLACE TABLE {table_name} ({columns_str})")

    assets = load_assets_from_modules([python_and_dbt_assets])

    materialize(assets, resources={"io_manager": io_manager, "dbt": dbt_resource})
