from app.database import engine
from app.models.base import Base
from app.models.country import Country


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")


if __name__ == "__main__":
    create_tables()