from sqlalchemy import ForeignKey, String #Foreign Key tells PostgreSQL that the value corresponds to an existing record in another table
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class Team(Base):
    __tablename__ = "teams"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(100), 
        nullable=False
    )
    country_id: Mapped[int] = mapped_column( 
        ForeignKey("countries.id"), # References the country associated with the team
        nullable=False
    )