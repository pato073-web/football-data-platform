from sqlalchemy import select

from datetime import date

from app.database import SessionLocal
from app.models.country import Country
from app.models.competition import Competition
from app.models.season import Season
from app.services.api_football import get_from_api

params = {
    "id":135,
    "season": 2024
}

leagues = get_from_api(
    "leagues",
    params=params
)

league_data = leagues[0]
api_league = league_data["league"]
api_country = league_data["country"]
api_season = league_data["seasons"][0]

print(api_league)
print(api_country)
print(api_season)

db = SessionLocal()

try:
    statement = select(Country).where(
        Country.code == api_country["code"]
    )

    country = db.scalar(statement)

    if country is None:
        country = Country(
            name = api_country["name"],
            code = api_country["code"]
        )
        db.add(country)
        db.commit()
        db.refresh(country)

        print("Country created", country.name)
    else:
        print("Country already exists", country.name)

    statement = select(Competition).where(
        Competition.api_football_id == api_league["id"]
    )
    competition = db.scalar(statement)

    if competition is None:
        competition = Competition(
            name = api_league["name"],
            country_id=country.id,
            api_football_id = api_league["id"]
        )
        db.add(competition)
        db.commit()
        db.refresh(competition)
        
        print("Competition created", competition.name)
    else:
        print("Competition already exists", competition.name)

    start_date = date.fromisoformat(api_season["start"])
    end_date = date.fromisoformat(api_season["end"])

    season_name = f"{api_season['year']}/{api_season['year'] + 1}"

    statement = select(Season).where(
        Season.competition_id == competition.id,
        Season.start_date == start_date,
        Season.end_date == end_date
    )

    season = db.scalar(statement)

    if season is None:
        season = Season(
            competition_id = competition.id,
            name = season_name,
            start_date = start_date,
            end_date = end_date
        )
        db.add(season)
        db.commit()
        db.refresh(season)

        print("Season created:", season.name)
    else:
        print("Season already exists:", season.name)
finally:
    db.close()