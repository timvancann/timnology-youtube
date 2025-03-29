from __future__ import annotations

from datetime import datetime, timezone

import enum
from sqlmodel import Field, SQLModel

class Region(enum.Enum):
    kanto = "Kanto"
    johto = "Johto"


class Pokemon(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    name: str
    number: int
    region: Region

