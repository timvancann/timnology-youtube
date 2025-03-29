from contextlib import asynccontextmanager
from fastapi import FastAPI

from blazing.db import create_db_and_tables
from blazing.routes import pokemon

@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(pokemon.router)
