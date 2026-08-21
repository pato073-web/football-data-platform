from datetime import date #Import the class date from the datetime module to represent dates in the Season model
from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class Season(Base):
    __tablename__ = "seasons"

    id: Mapped[int] = mapped_column(primary_key=True)

    competition_id: Mapped[int] = mapped_column(
        ForeignKey("competitions.id"), # References the competition associated with the season
        nullable=False
    )
    name: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )

    end_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )