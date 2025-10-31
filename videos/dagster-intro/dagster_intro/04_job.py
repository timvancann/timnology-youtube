from pathlib import Path
import polars as pl
import dagster as dg
from dagster_duckdb_polars import DuckDBPolarsIOManager


@dg.asset(io_manager_key="io_manager")
def plays() -> pl.DataFrame:
    date = Path("2025/10/16")
    df = pl.read_csv(date / "plays.csv")
    return df


io_manager = DuckDBPolarsIOManager(database="db.duckdb")
plays_job = dg.define_asset_job("plays_job", selection=["plays"])


def definitions() -> dg.Definitions:
    return dg.Definitions(
        assets=[plays], resources={"io_manager": io_manager}, jobs=[plays_job]
    )
