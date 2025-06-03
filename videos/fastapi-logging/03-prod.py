# pyright: basic
import logging
import os
import sys
import httpx
import uvicorn
from fastapi import FastAPI, Request
import sentry_sdk
from loguru import logger

BETTERSTACK_TOKEN = os.getenv("BETTERSTACK_TOKEN")
SENTRY_TOKEN = os.getenv("SENTRY_TOKEN")


class MissingEnvironmentVariableError(Exception):
    pass


if not BETTERSTACK_TOKEN:
    raise MissingEnvironmentVariableError("Missing BETTERSTACK_TOKEN")
if not SENTRY_TOKEN:
    raise MissingEnvironmentVariableError("Missing SENTRY_TOKEN")


async def async_sink(message):
    async with httpx.AsyncClient() as client:
        await client.post(
            "https://s1332380.eu-nbg-2.betterstackdata.com",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {BETTERSTACK_TOKEN}",
            },
            json=message,
            timeout=5.0,
        )


ENV = os.getenv("ENV", "dev")
logger.remove()
if ENV == "dev":
    logger.add(sys.stdout)
elif ENV == "prod":
    logger.add(sys.stdout, serialize=True)
    sentry_sdk.init(
        dsn=SENTRY_TOKEN,
        send_default_pii=True,
    )
    logger.add(async_sink, serialize=True)


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        level: str | int
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


for name in logging.root.manager.loggerDict:
    if name in ("uvicorn"):
        uvicorn_logger = logging.getLogger(name)
        uvicorn_logger.handlers.clear()
        uvicorn_logger.setLevel(logging.INFO)
        uvicorn_logger.addHandler(InterceptHandler())


app = FastAPI(title="01. Basic Logging")


@app.get("/")
async def root(request: Request):
    logger.info("Health check requested")
    return {"status": "healthy"}


@app.get("/sentry-debug")
async def trigger_error():
    _ = 1 / 0


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)
