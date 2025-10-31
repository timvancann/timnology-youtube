from pathlib import Path
import polars as pl
import dagster as dg


@dg.asset
def plays() -> None:
    date = Path("2025/10/16")
    _ = pl.read_csv(date / "plays.csv")


def definitions():
    return dg.Definitions(
        assets=[plays],
    )
