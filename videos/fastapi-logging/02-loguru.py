# pyright: basic
import logging

import uvicorn
from fastapi import FastAPI, Request

from loguru import logger


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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_config=None)
