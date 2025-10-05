from pathlib import Path

import logging
import dagster as dg
from dagster_duckdb_polars import DuckDBPolarsIOManager
import polars as pl
import whisper

partitions_def = dg.DailyPartitionsDefinition(start_date="2025-10-01")

LANDING_FOLDER = Path(
    "/Users/timvancann/repos/youtube/timnology-yt/videos/dagster-transcriptions/landing/audio_video"
)

logger = logging.getLogger(__name__)
logger.setLevel("INFO")


@dg.asset(
    partitions_def=partitions_def,
    io_manager_key="duckdb_io_manager",
    metadata={"partition_expr": "ingest_date"},
)
def transcription_asset(context: dg.AssetExecutionContext) -> pl.DataFrame | None:
    partition = context.partition_key
    folder = LANDING_FOLDER / partition.replace("-", "/")
    context.log.info(f"Scanning path {folder}")

    files = list(folder.glob("*.mkv"))
    context.log.info(f"files found: {list(files)}")

    rows = []
    for f in files:
        try:
            transcription = transcribe_with_whisper(f)
            rows.append(
                {
                    "file": str(f),
                    "ingest_date": partition,
                    "transcript": transcription["text"],
                }
            )
        except TranscriptionError:
            pass

    if len(rows) > 0:
        return pl.DataFrame(rows)
    return None


class TranscriptionError(Exception):
    pass


def transcribe_with_whisper(audio_fn: Path, model_name: str = "turbo"):
    model = whisper.load_model(model_name)
    try:
        result = model.transcribe(str(audio_fn))
    except Exception as e:
        raise TranscriptionError from e

    if "text" in result:
        return result

    raise TranscriptionError(result)


@dg.definitions
def defs():
    return dg.Definitions(
        assets=[transcription_asset],
        resources={
            "duckdb_io_manager": DuckDBPolarsIOManager(database="transcripts.duckdb")
        },
    )
