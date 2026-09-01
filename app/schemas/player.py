from datetime import date
from pydantic import BaseModel, ConfigDict

class PlayerBase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True
    )

    country_id: int
    name: str
    birth_date: date

class PlayerCreate(PlayerBase):
    pass

class PlayerResponse(PlayerBase):
    id: int

class PlayerUpdate(BaseModel):
    model_config=ConfigDict(
        extra="forbid"
    )
    country_id: int | None = None
    name: str | None = None
    birth_date: date | None = None