from sqlalchemy import ForeignKey, String #Foreign Key tells PostgreSQL that the value corresponds to an existing record in another table
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base

class Competition(Base):
    __tablename__ = "competitions"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(
        String(150), 
        nullable=False
    )
    country_id: Mapped[int | None] = mapped_column( #It can be a number or it can have no value, that's why None is used. We did this because there can be international competitions that do not belong to a specific country, such as the Champions League
        ForeignKey("countries.id"), # References the country associated with the competition
        nullable=True
    )


