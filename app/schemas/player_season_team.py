from datetime import date
from pydantic import BaseModel, ConfigDict

class PlayerSeasonTeamBase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True
    )

    player_id: int
    season_team_id: int
    start_date: date
    end_date: date | None = None

class PlayerSeasonTeamCreate(PlayerSeasonTeamBase):
    pass

class PlayerSeasonTeamResponse(PlayerSeasonTeamBase):
    id: int

class PlayerSeasonTeamUpdate(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )

    start_date: date | None = None
    end_date: date | None = None