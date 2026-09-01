from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.competition import Competition
from app.models.country import Country
from app.schemas.competition import CompetitionCreate, CompetitionResponse, CompetitionUpdate

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

@router.put("/{competition_id}", response_model=CompetitionResponse)
def update_competition(
    competition_id:int,
    competition_data:CompetitionUpdate,
    db:Session=Depends(get_db)
):
    competition = db.get(Competition, competition_id)
    if competition is None:
        raise HTTPException(
            status_code=404,
            detail="Competition not found"
        )
    
    update_data = competition_data.model_dump(exclude_unset=True)

    if "country_id" in update_data:
        if update_data["country_id"] is not None:
            country = db.get(Country, update_data["country_id"])
            if country is None:
                raise HTTPException(
                    status_code=404,
                    detail="Country not found"
                )

    if "name" in update_data and update_data["name"] is None:
        raise HTTPException(
            status_code=400,
            detail="Name cannot be null"
        )
    
    for field, value in update_data.items():
        setattr(competition, field, value)

    db.commit()
    db.refresh(competition)
    return competition

@router.delete("/{competition_id}", response_model=CompetitionResponse)
def delete_competition(
    competition_id:int,
    db: Session = Depends(get_db)
):
    competition = db.get(Competition, competition_id)
    if competition is None:
        raise HTTPException(
            status_code=404,
            detail="Competition not found"
        )
    try:
        db.delete(competition)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Competition cannot be deleted because it is being used."
        )
    return competition