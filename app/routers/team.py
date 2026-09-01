from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.team import Team
from app.models.country import Country
from app.schemas.team import TeamCreate, TeamResponse, TeamUpdate

router = APIRouter(
    prefix="/teams",
    tags=["Teams"]
)

@router.get("/", response_model=list[TeamResponse])
def get_teams(db: Session = Depends(get_db)):
    statement = select(Team)
    teams = db.scalars(statement).all()
    return teams

@router.get("/{team_id}", response_model=TeamResponse)
def get_team(
    team_id: int,
    db: Session = Depends(get_db)
):
    team = db.get(Team, team_id)
    if team is None:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )
    return team

@router.post("/", response_model=TeamResponse, status_code=201)
def create_team(
    team_data: TeamCreate,
    db: Session = Depends(get_db)
):

    country = db.get(Country, team_data.country_id)

    if country is None:
        raise HTTPException(
            status_code=404,
            detail = "Country not found"
        )

    team = Team(
        name=team_data.name,
        country_id=team_data.country_id,
    )

    db.add(team)
    db.commit()
    db.refresh(team)

    return team

@router.put("/{team_id}", response_model=TeamResponse)
def update_team(
    team_id:int,
    team_data: TeamUpdate,
    db: Session= Depends(get_db)
):
    team = db.get(Team, team_id)
    if team is None:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )

    update_data = team_data.model_dump(exclude_unset=True)

    if "country_id" in update_data:
        if update_data["country_id"] is None:
            raise HTTPException(
                status_code=400,
                detail="CountryID cannot be null"
            )
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
        setattr(team, field, value)

    db.commit()
    db.refresh(team)
    return team

@router.delete("/{team_id}", response_model=TeamResponse)
def delete_team(
    team_id:int,
    db:Session=Depends(get_db)
):
    team = db.get(Team,team_id)
    if team is None:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )
    try:
        db.delete(team)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Team cannot be deleted because it is being used"
        )
    return team