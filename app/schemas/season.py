from datetime import date

from pydantic import BaseModel, ConfigDict

class SeasonBase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True
    )

    competition_id: int
    name: str
    start_date: date
    end_date: date

class SeasonCreate(SeasonBase):
    pass

class SeasonResponse(SeasonBase):
    id: int