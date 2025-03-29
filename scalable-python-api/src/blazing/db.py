from os import environ
from typing import Annotated

from fastapi import Depends
from sqlmodel import SQLModel, create_engine, Session

username = environ.get("POSTGRES_USER")
password = environ.get("POSTGRES_PASSWORD")
host = environ.get("POSTGRES_HOST")
db = environ.get("POSTGRES_DB")
postgres_url = f"postgresql://{username}:{password}@{host}:5432/{db}"

engine = create_engine(postgres_url)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionType = Annotated[Session, Depends(get_session)]
