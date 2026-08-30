from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.team import Team
from app.models.country import Country
from app.schemas.team import TeamCreate, TeamResponse

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
