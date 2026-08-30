from datetime import date, time
from pydantic import BaseModel, ConfigDict

class MatchBase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True
    )

    season_id: int
    home_team_id: int
    away_team_id: int
    match_date: date
    kickoff_time: time | None = None
    home_score: int | None = None
    away_score: int | None = None
    status: str
    round: str | None = None

class MatchCreate(MatchBase):
    pass

class MatchResponse(MatchBase):
    id: int