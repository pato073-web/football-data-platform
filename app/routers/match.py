from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.match import Match
from app.models.season import Season
from app.models.team import Team
from app.models.season_team import SeasonTeam
from app.schemas.match import MatchCreate, MatchResponse, MatchUpdate

router = APIRouter(
    prefix="/matches",
    tags=["Matches"]
)

@router.get("/", response_model=list[MatchResponse])
def get_matches(db: Session = Depends(get_db)):
    statement = select(Match)
    matches = db.scalars(statement).all()
    return matches

@router.get("/{match_id}", response_model=MatchResponse)
def get_match(
    match_id: int,
    db: Session = Depends(get_db)
):
    match = db.get(Match,match_id)
    if match is None:
        raise HTTPException(
            status_code=404,
            detail = "Match not found"
        )
    return match

@router.post("/", response_model=MatchResponse, status_code=201)
def create_match(
    match_data: MatchCreate,
    db: Session = Depends(get_db)
):
    season_id = db.get(Season, match_data.season_id)
    if season_id is None:
        raise HTTPException(
            status_code=404,
            detail="Season not found"
        )
    home_team_id = db.get(Team, match_data.home_team_id)
    if home_team_id is None:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )
    away_team_id = db.get(Team, match_data.away_team_id)
    if away_team_id is None:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )
    statement = select(SeasonTeam).where(
        SeasonTeam.season_id == match_data.season_id,
        SeasonTeam.team_id == match_data.home_team_id
    )
    home_season_team = db.scalar(statement)

    if home_season_team is None:
        raise HTTPException(
            status_code=400,
            detail="Home team is not registered in this season"
        )
    statement = select(SeasonTeam).where(
        SeasonTeam.season_id == match_data.season_id,
        SeasonTeam.team_id == match_data.away_team_id
    )
    away_season_team = db.scalar(statement)

    if away_season_team is None:
        raise HTTPException(
            status_code=400,
            detail="Away team is not registered in this season"
        )

    if match_data.home_team_id == match_data.away_team_id:
        raise HTTPException(
            status_code=400,
            detail = "Home team and away team must be different"
        )

    match = Match(
        season_id = match_data.season_id,
        home_team_id = match_data.home_team_id,
        away_team_id = match_data.away_team_id,
        match_date = match_data.match_date,
        kickoff_time = match_data.kickoff_time,
        home_score = match_data.home_score,
        away_score = match_data.away_score,
        status = match_data.status,
        round = match_data.round
    )

    db.add(match)
    db.commit()
    db.refresh(match)

    return match

@router.put("/{match_id}", response_model=MatchResponse)
def update_match(
    match_id:int,
    match_data:MatchUpdate,
    db: Session = Depends(get_db)
):
    match = db.get(Match,match_id)
    if match is None:
        raise HTTPException(
            status_code=404,
            detail="Match not found"
        )
    update_data = match_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(match,field,value)

    db.commit()
    db.refresh(match)
    return match

@router.delete("/{match_id}", response_model=MatchResponse)
def delete_match(
    match_id: int,
    db: Session = Depends(get_db)
):
    match = db.get(Match, match_id)
    if match is None:
        raise HTTPException(
            status_code=404,
            detail="Match not found"
        )
    db.delete(match)
    db.commit()
    return match
