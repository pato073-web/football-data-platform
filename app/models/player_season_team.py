from datetime import date

from sqlalchemy import Date, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class PlayerSeasonTeam(Base):
    __tablename__ = "player_season_teams"

    id: Mapped[int] = mapped_column(primary_key=True)

    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id"),
        nullable=False
    )

    season_team_id: Mapped[int] = mapped_column(
        ForeignKey("season_teams.id"),
        nullable=False
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    end_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )