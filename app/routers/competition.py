from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.competition import Competition
from app.models.country import Country
from app.schemas.competition import CompetitionCreate, CompetitionResponse

router = APIRouter( 
    prefix="/competitions",
    tags=["Competitions"]
)

@router.get("/", response_model=list[CompetitionResponse])
def get_competitions(db: Session = Depends(get_db)):
    statement = select(Competition)
    competitions = db.scalars(statement).all()

    return competitions

@router.get("/{competition_id}", response_model=CompetitionResponse)
def get_competition(
    competition_id: int,
    db: Session = Depends(get_db)
):
    competition = db.get(Competition, competition_id)
    if competition is None:
        raise HTTPException(
            status_code=404,
            detail="Competition not found"
        )
    return competition

@router.post("/", response_model=CompetitionResponse, status_code=201)
def create_competition(
    competition_data: CompetitionCreate,
    db: Session = Depends(get_db)
):
    if competition_data.country_id is not None:
        country = db.get(Country, competition_data.country_id)

        if country is None:
            raise HTTPException(
                status_code=404,
                detail="Country not found"
            )

    competition = Competition(
        name=competition_data.name,
        country_id=competition_data.country_id
    )

    db.add(competition)
    db.commit()
    db.refresh(competition)

    return competition