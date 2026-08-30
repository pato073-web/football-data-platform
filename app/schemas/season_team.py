from pydantic import BaseModel, ConfigDict

class SeasonTeamBase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True
    )

    season_id:int
    team_id:int

class SeasonTeamCreate(SeasonTeamBase):
    pass

class SeasonTeamResponse(SeasonTeamBase):
    id: int