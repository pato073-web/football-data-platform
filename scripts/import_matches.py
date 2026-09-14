from datetime import datetime

from sqlalchemy import select

from app.database import SessionLocal
from app.models.competition import Competition
from app.models.season import Season
from app.models.team import Team
from app.models.match import Match
from app.services.api_football import get_from_api


params = {
    "league": 135,
    "season": 2024
}

fixtures = get_from_api(
    "fixtures",
    params=params
)

print("Fixtures found", len(fixtures))

status_mapping = {
    "NS": "scheduled",
    "TBD": "scheduled",
    "1H": "live",
    "HT": "live",
    "2H": "live",
    "ET": "live",
    "P": "live",
    "FT": "finished",
    "AET": "finished",
    "PEN": "finished",
    "PST": "postponed",
    "CANC": "cancelled"
}

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

    for fixture_data in fixtures:

        api_fixture = fixture_data["fixture"]
        api_league = fixture_data["league"]
        api_teams = fixture_data["teams"]
        api_goals = fixture_data["goals"]


        match_datetime = datetime.fromisoformat(
            api_fixture["date"]
        )

        match_date = match_datetime.date()
        kickoff_time = match_datetime.time()

        status = status_mapping.get(
        api_fixture["status"]["short"]
        )

        if status is None:
            raise ValueError(
                f"Unknown match status: {api_fixture['status']['short']}"
            )

        home_team = db.scalar(
            select(Team).where(
                Team.api_football_id == api_teams["home"]["id"]
            )
        )

        away_team = db.scalar(
            select(Team).where(
                Team.api_football_id == api_teams["away"]["id"]
            )
        )

        if home_team is None:
            raise ValueError ("Home Team does not exist")

        if away_team is None:
            raise ValueError ("Away Team does not exist")

        match = db.scalar(
            select(Match).where(
                Match.api_football_id == api_fixture["id"]
            )
        )

        if match is None:
            match = Match(
                api_football_id = api_fixture["id"],
                season_id = season.id,
                home_team_id = home_team.id,
                away_team_id = away_team.id,
                match_date = match_date,
                kickoff_time = kickoff_time,
                home_score = api_goals["home"],
                away_score = api_goals["away"],
                status = status,
                round = api_league["round"]
            )

            db.add(match)
            db.commit()

            print("Match created:", home_team.name, "vs", away_team.name)

        else:
            print("Match already exists:", home_team.name, "vs", away_team.name)

finally:
    db.close()
