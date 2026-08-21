from datetime import date
from sqlalchemy import Date, ForeignKey, String 
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100), 
        nullable=False
    )
    country_id: Mapped[int] = mapped_column( 
        ForeignKey("countries.id"), #references the players nationality
        nullable=False
    )
    birth_date: Mapped[date] = mapped_column(
        Date,
        nullable=False
    )
