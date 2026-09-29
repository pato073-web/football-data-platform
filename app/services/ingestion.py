from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.country import Country
from app.models.competition import Competition
from app.models.season import Season
from app.models.team import Team
from app.models.season_team import SeasonTeam
from app.models.match import Match
from app.services.api_football import get_from_api

def import_competition(
        db:Session,
        league_id: int,
        season_year: int
):
    params = {
        "id": league_id,
        "season": season_year
    }

    leagues = get_from_api (
        "leagues",
        params = params
    )

    if not leagues:
        raise ValueError(
            f"No competition found for League {league_id}, "
            f"season {season_year}"
        )

    league_data = leagues[0]

    api_league = league_data["league"]
    api_country = league_data["country"]
    api_season = league_data["seasons"][0]

    try:
        country = db.scalar(
            select(Country).where(
                Country.code == api_country["code"]
            )
        )

        if country is None:
            country = Country(
                name = api_country["name"],
                code = api_country["code"]
            )

            db.add(country)
            db.flush()

        competition = db.scalar(
            select(Competition).where(
                Competition.api_football_id == api_league["id"]
            )
        )

        if competition is None:
            competition = Competition(
                name = api_league["name"],
                country_id=country.id,
                api_football_id=api_league["id"]
            )

            db.add(competition)
            db.flush()

        start_date = date.fromisoformat(
            api_season["start"]
        )

        end_date = date.fromisoformat(
            api_season["end"]
        )

        season_name = (
            f"{api_season['year']}/"
            f"{api_season['year'] + 1}"
        )

        season = db.scalar(
            select(Season).where(
                Season.competition_id == competition.id,
                Season.start_date == start_date,
                Season.end_date == end_date
            )
        )

        if season is None:
            season = Season(
                name = season_name,
                competition_id = competition.id,
                start_date = start_date,
                end_date = end_date
            )

            db.add(season)
            db.flush()

        db.commit()

        return country, competition, season

    except Exception:
        db.rollback()
        raise

def import_teams(
        db:Session,
        league_id : int,
        season_year:int,
        country : Country
):
    try:
        api_teams = get_from_api(
            "teams",
            params={
                "league": league_id,
                "season": season_year
            }
        )

        teams = []

        for team_data in api_teams:
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
                db.flush()

            teams.append(team)

        db.commit()

        return teams

    except Exception:
        db.rollback()
        raise

def import_season_teams(
        db:Session,
        season:Season,
        teams:list[Team]
):
    try:
        season_teams = []

        for team in teams:
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
                db.flush()

            season_teams.append(season_team)

        db.commit()

        return season_teams
    except Exception:
        db.rollback()
        raise

def import_matches(
        db:Session,
        league_id:int,
        season_year:int,
        season:Season
):
    fixtures = get_from_api(
        "fixtures",
        params={
            "league": league_id,
            "season": season_year
        }
    )

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

    try:
        matches = []

        for fixture_data in fixtures:
            api_fixture = fixture_data["fixture"]
            api_league = fixture_data["league"]
            api_teams = fixture_data["teams"]
            api_goals = fixture_data['goals']

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
                    f"Unknown match status: "
                    f"{api_fixture['status']['short']}"
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
                raise ValueError(
                    f"Home team does not exist:"
                    f"{api_teams['home']['name']}"
                )
            if away_team is None:
                raise ValueError(
                    f"Away team does not exist:"
                    f"{api_teams['away']['name']}"
                )

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

            else:
                match.season_id = season.id
                match.home_team_id = home_team.id
                match.away_team_id = away_team.id
                match.match_date = match_date
                match.kickoff_time = kickoff_time
                match.home_score = api_goals["home"]
                match.away_score = api_goals["away"]
                match.status = status
                match.round = api_league["round"]

            matches.append(match)

        db.commit()

        return matches

    except Exception:
        db.rollback()
        raise

def import_league_data(
    db: Session,
    league_id: int,
    season_year: int
):
    country, competition, season = import_competition(
        db=db,
        league_id = league_id,
        season_year = season_year
    )

    teams = import_teams(
        db = db,
        league_id= league_id,
        season_year= season_year,
        country= country
    )

    season_teams = import_season_teams(
        db = db,
        season = season,
        teams = teams
    )

    matches = import_matches(
        db = db,
        league_id = league_id,
        season_year = season_year,
        season = season
    )

    return {
        "country": country,
        "competition" : competition,
        "season" : season,
        "teams" : teams,
        "season_teams" : season_teams,
        "matches" : matches
    }