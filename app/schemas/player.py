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