import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.models.base import Base
from app.models.country import Country
from app.models.competition import Competition
from app.models.season import Season
from app.models.team import Team
from app.models.season_team import SeasonTeam
from app.models.player import Player
from app.models.player_season_team import PlayerSeasonTeam
from app.models.match import Match


@pytest.fixture
def db():
    engine = create_engine(
        "sqlite://",
        connect_args={
            "check_same_thread": False
        },
        poolclass=StaticPool
    )

    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False
    )

    session = TestingSessionLocal()

    try:
        yield session

    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)