from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class SeasonTeam(Base):
    __tablename__ = "season_teams"

    __table_args__ = (
        UniqueConstraint(
            "season_id",
            "team_id",
            name="uq_season_team"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    season_id: Mapped[int] = mapped_column(
        ForeignKey("seasons.id"),
        nullable=False
    )

    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"),
        nullable=False
    )