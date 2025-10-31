from pathlib import Path
import polars as pl
import dagster as dg
from dagster_duckdb_polars import DuckDBPolarsIOManager

daily_partitions = dg.DailyPartitionsDefinition(start_date="2024-01-01")


@dg.asset(
    io_manager_key="io_manager",
    partitions_def=daily_partitions,
    metadata={"partition_expr": "date"},
)
def plays(context: dg.AssetExecutionContext) -> pl.DataFrame:
    partition_datetime = context.partition_time_window.start

    date = (
        Path(partition_datetime.strftime("%Y"))
        / partition_datetime.strftime("%m")
        / partition_datetime.strftime("%d")
    )
    df = pl.read_csv(date / "plays.csv").with_columns(
        date=partition_datetime.strftime("%Y-%m-%d")
    )
    return df


io_manager = DuckDBPolarsIOManager(database="db.duckdb")
plays_job = dg.define_asset_job("plays_job", selection=["plays"])
asset_partitioned_schedule = dg.build_schedule_from_partitioned_job(
    plays_job,
    default_status=dg.DefaultScheduleStatus.RUNNING,
)


def definitions() -> dg.Definitions:
    return dg.Definitions(
        assets=[plays],
        resources={"io_manager": io_manager},
        jobs=[plays_job],
        schedules=[asset_partitioned_schedule],
    )
