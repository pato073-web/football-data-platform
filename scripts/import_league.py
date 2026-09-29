from app.database import SessionLocal
from app.services.ingestion import import_league_data

db = SessionLocal()

try:
    result = import_league_data(
        db = db,
        league_id = 135,
        season_year = 2024
    )

    print("Import completed")
    print("Country:", result["country"].name)
    print("Competition:", result["competition"].name)
    print("Season:", result["season"].name)
    print("Teams:", len(result["teams"]))
    print("Season teams:", len(result["season_teams"]))
    print("Matches:", len(result["matches"]))

finally:
    db.close()