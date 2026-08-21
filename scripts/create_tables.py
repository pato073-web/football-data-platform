from app.database import engine
from app.models.base import Base
from app.models.country import Country
from app.models.competition import Competition
from app.models.season import Season
from app.models.team import Team
from app.models.season_team import SeasonTeam
from app.models.player import Player
from app.models.player_season_team import PlayerSeasonTeam
from app.models.match import Match


def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")


if __name__ == "__main__":
    create_tables()