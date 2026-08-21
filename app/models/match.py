from datetime import date, time

from sqlalchemy import CheckConstraint, Date, ForeignKey, String, Time
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class Match(Base):
    __tablename__ = "matches"

    __table_args__ = (
        CheckConstraint(
            "home_team_id <> away_team_id", # Ensures that the home team and away team are not the same
            name = "ck_match_different_teams"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    season_id: Mapped[int] = mapped_column(
        ForeignKey("seasons.id"), # References the season associated with the match
        nullable=False
    )

    home_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"),
        nullable=False
    )

    away_team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"),
        nullable=False
    )
    
    match_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    kickoff_time: Mapped[time | None] = mapped_column(
        Time,
        nullable=True
    )

    home_score: Mapped[int | None] = mapped_column(
        nullable=True
    )

    away_score: Mapped[int | None] = mapped_column(
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    round: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )