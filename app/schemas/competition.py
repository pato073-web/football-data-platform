from pydantic import BaseModel, ConfigDict

class CompetitionBase(BaseModel):
    model_config=ConfigDict(
        extra="forbid",
        from_attributes=True,
    )

    name: str
    country_id: int | None = None

class CompetitionCreate(CompetitionBase):
    pass

class CompetitionResponse(CompetitionBase):
    id: int

class CompetitionUpdate(BaseModel):
    model_config=ConfigDict(
        extra="forbid"
    )
    name: str | None = None
    country_id:int | None = None