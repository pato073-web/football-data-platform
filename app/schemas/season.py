from datetime import date

from pydantic import BaseModel, ConfigDict, model_validator

class SeasonBase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True
    )

    competition_id: int
    name: str
    start_date: date
    end_date: date

    @model_validator(mode="after")
    def validate_dates(self):
        if self.start_date >= self.end_date:
            raise ValueError("Start_date must be before end_date")
        
        return self

class SeasonCreate(SeasonBase):
    pass

class SeasonResponse(SeasonBase):
    id: int

class SeasonUpdate(BaseModel):
    model_config=ConfigDict(
        extra="forbid"
    )
    competition_id:int | None = None
    name:str | None = None
    start_date:date | None = None
    end_date:date | None = None