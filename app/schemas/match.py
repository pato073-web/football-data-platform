from datetime import date, time
from pydantic import BaseModel, ConfigDict, Field
from typing import Literal

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
    home_score: int | None = Field(default=None, ge=0)
    away_score: int | None = Field(default=None, ge=0)
    status: Literal[
        "scheduled",
        "live",
        "finished",
        "postponed",
        "cancelled"
    ]
    round: str | None = None

class MatchCreate(MatchBase):
    pass

class MatchResponse(MatchBase):
    id: int

class MatchUpdate(BaseModel):
    model_config = ConfigDict(
        extra="forbid"
    )

    kickoff_time: time | None = None
    home_score: int | None = Field(default=None, ge=0)
    away_score: int | None = Field(default=None, ge=0)
    status: Literal[
        "scheduled",
        "live",
        "finished",
        "postponed",
        "cancelled"
    ] | None = None
    round: str | None = None