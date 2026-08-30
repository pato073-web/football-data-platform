from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.season import Season
from app.models.competition import Competition
from app.schemas.season import SeasonCreate, SeasonResponse

router = APIRouter(
    prefix="/seasons",
    tags=["Seasons"]
)

@router.get("/", response_model=list[SeasonResponse])
def get_seasons(db: Session = Depends(get_db)):
    statement = select(Season)
    seasons = db.scalars(statement).all()

    return seasons

@router.get("/{season_id}", response_model=SeasonResponse)
def get_season(
    season_id: int,
    db: Session = Depends(get_db)
):
    season = db.get(Season, season_id)
    if season is None:
        raise HTTPException(
            status_code=404,
            detail="Season not found"
        )
    return season

@router.post("/", response_model=SeasonResponse, status_code=201)
def create_season(
    season_data: SeasonCreate,
    db: Session = Depends(get_db)
):
    
    competition = db.get(Competition, season_data.competition_id)

    if competition is None:
        raise HTTPException(
            status_code=404,
            detail="Competition not found"
        )

    season = Season(
        name=season_data.name,
        competition_id=season_data.competition_id,
        start_date=season_data.start_date,
        end_date=season_data.end_date
    )

    db.add(season)
    db.commit()
    db.refresh(season)

    return season