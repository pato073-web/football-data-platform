from pydantic import BaseModel, ConfigDict

class TeamBase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True
    )

    country_id: int
    name: str

class TeamCreate(TeamBase):
    pass

class TeamResponse(TeamBase):
    id: int

class TeamUpdate(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )
    name: str | None = None
    country_id: int | None = None