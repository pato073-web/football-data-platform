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