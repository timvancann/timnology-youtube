from pathlib import Path
import polars as pl
import dagster as dg
from dagster_duckdb import DuckDBResource


@dg.asset
def plays(duckdb: DuckDBResource) -> None:
    date = Path("2025/10/16")
    df = pl.read_csv(date / "plays.csv")
    df.write_database(table_name="plays", connection=f"duckdb:///{duckdb.database}")


duckdb_resource = DuckDBResource(database="db.duckdb")


def definitions() -> dg.Definitions:
    return dg.Definitions(
        assets=[plays],
        resources={"duckdb": duckdb_resource},
    )
