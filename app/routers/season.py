from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.season import Season
from app.models.competition import Competition
from app.schemas.season import SeasonCreate, SeasonResponse, SeasonUpdate

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

@router.put("/{season_id}", response_model=SeasonResponse)
def update_season(
    season_id:int,
    season_data:SeasonUpdate,
    db:Session=Depends(get_db)
):
    season = db.get(Season, season_id)
    if season is None:
        raise HTTPException(
            status_code=404,
            detail="Season not found"
        )
    update_data = season_data.model_dump(exclude_unset=True)

    if "competition_id" in update_data:
        if update_data["competition_id"] is None:
            raise HTTPException(
                status_code=400,
                detail="CompetitionID cannot be null"
            )
        competition=db.get(Competition, update_data["competition_id"])
        if competition is None:
            raise HTTPException(
                status_code=404,
                detail="Competition not found"
            )
    new_start_date = update_data.get("start_date", season.start_date)
    new_end_date = update_data.get("end_date", season.end_date)
    if new_start_date is None or new_end_date is None:
        raise HTTPException(
            status_code=400,
            detail="Season dates cannot be null"
        )
    if new_start_date >= new_end_date:
        raise HTTPException(
            status_code=400,
            detail="StartDate must be before end_date"
        )

    if "name" in update_data and update_data["name"] is None:
            raise HTTPException(
                status_code=400,
                detail="Name cannot be null"
            )

    for field, value in update_data.items():
        setattr(season, field, value)

    db.commit()
    db.refresh(season)
    return season

@router.delete("/{season_id}", response_model=SeasonResponse)
def delete_season(
    season_id:int,
    db:Session = Depends(get_db)
):
    season = db.get(Season, season_id)
    if season is None:
        raise HTTPException(
            status_code=404,
            detail="Season not found"
        )
    try:
        db.delete(season)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Season cannot be deleted because it is being used"
        )
    return season