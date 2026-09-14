from sqlalchemy import select

from app.database import SessionLocal
from app.models.country import Country
from app.models.team import Team
from app.services.api_football import get_from_api

params = {
    "league" : 135,
    "season" : 2024
}

teams = get_from_api(
    "teams",
    params=params
)

db = SessionLocal()

try:
    country = db.scalar(
        select(Country).where(Country.name == "Italy")
    )
    if country is None:
        raise ValueError("Italy does not exist in the database")
    for team_data in teams:
        api_team = team_data["team"]

        team = db.scalar(
            select(Team).where(
                Team.api_football_id == api_team["id"]
            )
        )
        if team is None:
            team = Team(
                api_football_id = api_team["id"],
                name = api_team["name"],
                country_id = country.id
            )

            db.add(team)
            db.commit()
            db.refresh(team)

            print("Team created:", team.name)

        else:
            print("Team already exists:", team.name)
finally:
    db.close() 