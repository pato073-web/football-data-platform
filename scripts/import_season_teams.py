from sqlalchemy import select

from app.database import SessionLocal
from app.models.competition import Competition
from app.models.season import Season
from app.models.team import Team
from app.models.season_team import SeasonTeam

from app.services.api_football import get_from_api

db = SessionLocal()

try:
    competition = db.scalar(
        select(Competition).where(
            Competition.api_football_id == 135
        )
    )
    if competition is None:
        raise ValueError("Serie A does not exist")
    season = db.scalar(
        select(Season).where(
            Season.competition_id == competition.id,
            Season.name == "2024/2025"
        )
    )
    if season is None:
        raise ValueError("Season does not exist")

    api_teams = get_from_api(
        "teams",
        params = {
            "league": 135,
            "season":2024
        }
    )
    for team_data in api_teams:
        api_team = team_data["team"]

        team = db.scalar(
            select(Team).where(
                Team.api_football_id == api_team["id"]
            )
        )
        if team is None:
            print("Team not found: ", api_team["name"])
            continue

        season_team = db.scalar(
            select(SeasonTeam).where(
                SeasonTeam.season_id == season.id,
                SeasonTeam.team_id == team.id
            )
        )

        if season_team is None:
            season_team = SeasonTeam(
                season_id = season.id,
                team_id = team.id
            )

            db.add(season_team)
            db.commit()
            db.refresh(season_team)

            print("Added to season:", team.name)
        else:
            print("Already in season", team.name)

finally:
    db.close()