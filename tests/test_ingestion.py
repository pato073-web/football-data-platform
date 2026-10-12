from datetime import date

from sqlalchemy import select

from app.models.competition import Competition
from app.models.country import Country
from app.models.match import Match
from app.models.season import Season
from app.models.season_team import SeasonTeam
from app.models.team import Team

from app.services.ingestion import (
    import_competition,
    import_matches,
    import_season_teams,
    import_teams,
)


def test_pytest_is_working():
    assert 1 + 1 == 2


def test_import_competition(db, monkeypatch):
    fake_api_response = [
        {
            "league": {
                "id": 135,
                "name": "Serie A",
                "type": "League"
            },
            "country": {
                "name": "Italy",
                "code": "IT"
            },
            "seasons": [
                {
                    "year": 2024,
                    "start": "2024-08-17",
                    "end": "2025-05-25"
                }
            ]
        }
    ]

    def fake_get_from_api(endpoint, params=None):
        return fake_api_response

    monkeypatch.setattr(
        "app.services.ingestion.get_from_api",
        fake_get_from_api
    )

    country, competition, season = import_competition(
        db=db,
        league_id=135,
        season_year=2024
    )

    assert country.name == "Italy"
    assert country.code == "IT"

    assert competition.name == "Serie A"
    assert competition.api_football_id == 135
    assert competition.country_id == country.id

    assert season.name == "2024/2025"
    assert season.competition_id == competition.id


def test_import_competition_is_idempotent(db, monkeypatch):
    fake_api_response = [
        {
            "league": {
                "id": 135,
                "name": "Serie A",
                "type": "League"
            },
            "country": {
                "name": "Italy",
                "code": "IT"
            },
            "seasons": [
                {
                    "year": 2024,
                    "start": "2024-08-17",
                    "end": "2025-05-25"
                }
            ]
        }
    ]

    def fake_get_from_api(endpoint, params=None):
        return fake_api_response

    monkeypatch.setattr(
        "app.services.ingestion.get_from_api",
        fake_get_from_api
    )

    import_competition(
        db=db,
        league_id=135,
        season_year=2024
    )

    import_competition(
        db=db,
        league_id=135,
        season_year=2024
    )

    countries = db.scalars(
        select(Country)
    ).all()

    competitions = db.scalars(
        select(Competition)
    ).all()

    seasons = db.scalars(
        select(Season)
    ).all()

    assert len(countries) == 1
    assert len(competitions) == 1
    assert len(seasons) == 1


def test_import_teams(db, monkeypatch):
    country = Country(
        name="Italy",
        code="IT"
    )

    db.add(country)
    db.commit()
    db.refresh(country)

    fake_api_response = [
        {
            "team": {
                "id": 505,
                "name": "Inter",
                "country": "Italy"
            }
        },
        {
            "team": {
                "id": 489,
                "name": "AC Milan",
                "country": "Italy"
            }
        }
    ]

    def fake_get_from_api(endpoint, params=None):
        return fake_api_response

    monkeypatch.setattr(
        "app.services.ingestion.get_from_api",
        fake_get_from_api
    )

    teams = import_teams(
        db=db,
        league_id=135,
        season_year=2024,
        country=country
    )

    assert len(teams) == 2

    assert teams[0].name == "Inter"
    assert teams[0].api_football_id == 505
    assert teams[0].country_id == country.id

    assert teams[1].name == "AC Milan"
    assert teams[1].api_football_id == 489
    assert teams[1].country_id == country.id

    teams_in_database = db.scalars(
        select(Team)
    ).all()

    assert len(teams_in_database) == 2


def test_import_teams_is_idempotent(db, monkeypatch):
    country = Country(
        name="Italy",
        code="IT"
    )

    db.add(country)
    db.commit()
    db.refresh(country)

    fake_api_response = [
        {
            "team": {
                "id": 505,
                "name": "Inter",
                "country": "Italy"
            }
        },
        {
            "team": {
                "id": 489,
                "name": "AC Milan",
                "country": "Italy"
            }
        }
    ]

    def fake_get_from_api(endpoint, params=None):
        return fake_api_response

    monkeypatch.setattr(
        "app.services.ingestion.get_from_api",
        fake_get_from_api
    )

    import_teams(
        db=db,
        league_id=135,
        season_year=2024,
        country=country
    )

    import_teams(
        db=db,
        league_id=135,
        season_year=2024,
        country=country
    )

    teams = db.scalars(
        select(Team)
    ).all()

    assert len(teams) == 2

    inter = db.scalar(
        select(Team).where(
            Team.api_football_id == 505
        )
    )

    milan = db.scalar(
        select(Team).where(
            Team.api_football_id == 489
        )
    )

    assert inter is not None
    assert milan is not None

    assert inter.name == "Inter"
    assert milan.name == "AC Milan"


def test_import_season_teams(db):
    country = Country(
        name="Italy",
        code="IT"
    )

    db.add(country)
    db.flush()

    competition = Competition(
        name="Serie A",
        country_id=country.id,
        api_football_id=135
    )

    db.add(competition)
    db.flush()

    season = Season(
        competition_id=competition.id,
        name="2024/2025",
        start_date=date(2024, 8, 17),
        end_date=date(2025, 5, 25)
    )

    db.add(season)
    db.flush()

    inter = Team(
        api_football_id=505,
        name="Inter",
        country_id=country.id
    )

    milan = Team(
        api_football_id=489,
        name="AC Milan",
        country_id=country.id
    )

    db.add(inter)
    db.add(milan)
    db.commit()

    teams = [inter, milan]

    season_teams = import_season_teams(
        db=db,
        season=season,
        teams=teams
    )

    assert len(season_teams) == 2

    relationships = db.scalars(
        select(SeasonTeam)
    ).all()

    assert len(relationships) == 2

    assert season_teams[0].season_id == season.id
    assert season_teams[0].team_id == inter.id

    assert season_teams[1].season_id == season.id
    assert season_teams[1].team_id == milan.id


def test_import_season_teams_is_idempotent(db):
    country = Country(
        name="Italy",
        code="IT"
    )

    db.add(country)
    db.flush()

    competition = Competition(
        name="Serie A",
        country_id=country.id,
        api_football_id=135
    )

    db.add(competition)
    db.flush()

    season = Season(
        competition_id=competition.id,
        name="2024/2025",
        start_date=date(2024, 8, 17),
        end_date=date(2025, 5, 25)
    )

    db.add(season)
    db.flush()

    inter = Team(
        api_football_id=505,
        name="Inter",
        country_id=country.id
    )

    milan = Team(
        api_football_id=489,
        name="AC Milan",
        country_id=country.id
    )

    db.add(inter)
    db.add(milan)
    db.commit()

    teams = [inter, milan]

    import_season_teams(
        db=db,
        season=season,
        teams=teams
    )

    import_season_teams(
        db=db,
        season=season,
        teams=teams
    )

    relationships = db.scalars(
        select(SeasonTeam)
    ).all()

    assert len(relationships) == 2


def test_import_matches(db, monkeypatch):
    country = Country(
        name="Italy",
        code="IT"
    )

    db.add(country)
    db.flush()

    competition = Competition(
        name="Serie A",
        country_id=country.id,
        api_football_id=135
    )

    db.add(competition)
    db.flush()

    season = Season(
        competition_id=competition.id,
        name="2024/2025",
        start_date=date(2024, 8, 17),
        end_date=date(2025, 5, 25)
    )

    db.add(season)
    db.flush()

    inter = Team(
        api_football_id=505,
        name="Inter",
        country_id=country.id
    )

    milan = Team(
        api_football_id=489,
        name="AC Milan",
        country_id=country.id
    )

    db.add(inter)
    db.add(milan)
    db.commit()

    fake_api_response = [
        {
            "fixture": {
                "id": 123456,
                "date": "2024-09-22T18:45:00+00:00",
                "status": {
                    "short": "FT"
                }
            },
            "league": {
                "id": 135,
                "round": "Regular Season - 5"
            },
            "teams": {
                "home": {
                    "id": 505,
                    "name": "Inter"
                },
                "away": {
                    "id": 489,
                    "name": "AC Milan"
                }
            },
            "goals": {
                "home": 2,
                "away": 1
            }
        }
    ]

    def fake_get_from_api(endpoint, params=None):
        return fake_api_response

    monkeypatch.setattr(
        "app.services.ingestion.get_from_api",
        fake_get_from_api
    )

    matches = import_matches(
        db=db,
        league_id=135,
        season_year=2024,
        season=season
    )

    assert len(matches) == 1

    match = matches[0]

    assert match.api_football_id == 123456
    assert match.season_id == season.id
    assert match.home_team_id == inter.id
    assert match.away_team_id == milan.id

    assert match.home_score == 2
    assert match.away_score == 1

    assert match.status == "finished"
    assert match.round == "Regular Season - 5"

    matches_in_database = db.scalars(
        select(Match)
    ).all()

    assert len(matches_in_database) == 1


def test_import_matches_updates_existing_match(db, monkeypatch):
    country = Country(
        name="Italy",
        code="IT"
    )

    db.add(country)
    db.flush()

    competition = Competition(
        name="Serie A",
        country_id=country.id,
        api_football_id=135
    )

    db.add(competition)
    db.flush()

    season = Season(
        competition_id=competition.id,
        name="2024/2025",
        start_date=date(2024, 8, 17),
        end_date=date(2025, 5, 25)
    )

    db.add(season)
    db.flush()

    inter = Team(
        api_football_id=505,
        name="Inter",
        country_id=country.id
    )

    milan = Team(
        api_football_id=489,
        name="AC Milan",
        country_id=country.id
    )

    db.add(inter)
    db.add(milan)
    db.commit()

    fake_api_response = [
        {
            "fixture": {
                "id": 123456,
                "date": "2024-09-22T18:45:00+00:00",
                "status": {
                    "short": "NS"
                }
            },
            "league": {
                "id": 135,
                "round": "Regular Season - 5"
            },
            "teams": {
                "home": {
                    "id": 505,
                    "name": "Inter"
                },
                "away": {
                    "id": 489,
                    "name": "AC Milan"
                }
            },
            "goals": {
                "home": None,
                "away": None
            }
        }
    ]

    def fake_get_from_api(endpoint, params=None):
        return fake_api_response

    monkeypatch.setattr(
        "app.services.ingestion.get_from_api",
        fake_get_from_api
    )

    import_matches(
        db=db,
        league_id=135,
        season_year=2024,
        season=season
    )

    match = db.scalar(
        select(Match).where(
            Match.api_football_id == 123456
        )
    )

    assert match is not None
    assert match.status == "scheduled"
    assert match.home_score is None
    assert match.away_score is None

    fake_api_response[0]["fixture"]["status"]["short"] = "FT"
    fake_api_response[0]["goals"]["home"] = 2
    fake_api_response[0]["goals"]["away"] = 1

    import_matches(
        db=db,
        league_id=135,
        season_year=2024,
        season=season
    )

    matches = db.scalars(
        select(Match)
    ).all()

    assert len(matches) == 1

    updated_match = matches[0]

    assert updated_match.api_football_id == 123456
    assert updated_match.status == "finished"
    assert updated_match.home_score == 2
    assert updated_match.away_score == 1

def test_import_matches_rolls_back_on_error(db, monkeypatch):
    country = Country(
        name="Italy",
        code="IT"
    )

    db.add(country)
    db.flush()

    competition = Competition(
        name="Serie A",
        country_id=country.id,
        api_football_id=135
    )

    db.add(competition)
    db.flush()

    season = Season(
        competition_id=competition.id,
        name="2024/2025",
        start_date=date(2024, 8, 17),
        end_date=date(2025, 5, 25)
    )

    db.add(season)
    db.flush()

    inter = Team(
        api_football_id=505,
        name="Inter",
        country_id=country.id
    )

    milan = Team(
        api_football_id=489,
        name="AC Milan",
        country_id=country.id
    )

    db.add(inter)
    db.add(milan)
    db.commit()

    fake_api_response = [
        {
            "fixture": {
                "id": 123456,
                "date": "2024-09-22T18:45:00+00:00",
                "status": {
                    "short": "FT"
                }
            },
            "league": {
                "id": 135,
                "round": "Regular Season - 5"
            },
            "teams": {
                "home": {
                    "id": 505,
                    "name": "Inter"
                },
                "away": {
                    "id": 489,
                    "name": "AC Milan"
                }
            },
            "goals": {
                "home": 2,
                "away": 1
            }
        },
        {
            "fixture": {
                "id": 123457,
                "date": "2024-09-29T18:45:00+00:00",
                "status": {
                    "short": "UNKNOWN"
                }
            },
            "league": {
                "id": 135,
                "round": "Regular Season - 6"
            },
            "teams": {
                "home": {
                    "id": 489,
                    "name": "AC Milan"
                },
                "away": {
                    "id": 505,
                    "name": "Inter"
                }
            },
            "goals": {
                "home": None,
                "away": None
            }
        }
    ]

    def fake_get_from_api(endpoint, params=None):
        return fake_api_response

    monkeypatch.setattr(
        "app.services.ingestion.get_from_api",
        fake_get_from_api
    )

    try:
        import_matches(
            db=db,
            league_id=135,
            season_year=2024,
            season=season
        )

        assert False

    except ValueError as error:
        assert "Unknown match status" in str(error)

    matches = db.scalars(
        select(Match)
    ).all()

    assert len(matches) == 0