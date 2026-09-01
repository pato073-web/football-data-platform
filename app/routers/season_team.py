from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.season_team import SeasonTeam
from app.models.season import Season
from app.models.team import Team
from app.schemas.season_team import SeasonTeamCreate, SeasonTeamResponse

router = APIRouter(
    prefix="/season-teams",
    tags=["Season Teams"]
)

@router.get("/", response_model=list[SeasonTeamResponse])
def get_season_teams(db: Session = Depends(get_db)):
    statement = select(SeasonTeam)
    season_teams = db.scalars(statement).all()

    return season_teams

@router.get("/{season_team_id}", response_model=SeasonTeamResponse)
def get_season_teams(
    season_team_id: int,
    db: Session = Depends(get_db)
):
    seasonteam = db.get(SeasonTeam, season_team_id)
    if seasonteam is None:
        raise HTTPException(
            status_code=404,
            detail="SeasonTeam not found"
        )
    return seasonteam

@router.post("/", response_model=SeasonTeamResponse, status_code=201)
def create_seasonteam(
    season_team_data: SeasonTeamCreate,
    db: Session = Depends(get_db)
):
    season = db.get(Season, season_team_data.season_id)
    if season is None:
        raise HTTPException(
            status_code=404,
            detail="Season not found"
        )
    team = db.get(Team, season_team_data.team_id)
    if team is None:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )
    seasonteam = SeasonTeam(
        season_id=season_team_data.season_id,
        team_id=season_team_data.team_id
    )
    db.add(seasonteam)
    try:
        db.commit()
        db.refresh(seasonteam)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Team is already registered in this season"
        )

    return seasonteam

@router.delete("/{season_team_id}", response_model=SeasonTeamResponse)
def delete_season_team(
    season_team_id:int,
    db: Session=Depends(get_db)
):
    seasonteam = db.get(SeasonTeam,season_team_id)
    if seasonteam is None:
        raise HTTPException(
            status_code=404,
            detail="SeasonTeam not found"
        )
    try:
        db.delete(seasonteam)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="SeasonTeam cannot be deleted because it is being used"
        )
    return seasonteam