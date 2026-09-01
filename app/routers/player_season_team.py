from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.player_season_team import PlayerSeasonTeam
from app.models.player import Player
from app.models.season_team import SeasonTeam
from app.schemas.player_season_team import PlayerSeasonTeamCreate, PlayerSeasonTeamResponse, PlayerSeasonTeamUpdate

router = APIRouter(
    prefix="/player-season-teams",
    tags=["Player Season Teams"]
)

@router.get("/", response_model=list[PlayerSeasonTeamResponse])
def get_player_season_teams(db: Session = Depends(get_db)):
    statement = select(PlayerSeasonTeam)
    player_season_teams = db.scalars(statement).all()

    return player_season_teams

@router.get("/{player_season_team_id}", response_model=PlayerSeasonTeamResponse)
def get_player_season_team(
    player_season_team_id: int,
    db: Session = Depends(get_db)
):
    player_season_team = db.get(PlayerSeasonTeam, player_season_team_id)
    if player_season_team is None:
        raise HTTPException(
            status_code=404,
            detail="Player Season Team not found"
        )
    return player_season_team

@router.post("/", response_model=PlayerSeasonTeamResponse, status_code=201)
def create_player_season_team(
    player_season_team_data: PlayerSeasonTeamCreate,
    db: Session = Depends(get_db)
):
    player= db.get(Player, player_season_team_data.player_id)
    if player is None:
        raise HTTPException(
            status_code=404,
            detail = "Player not found"
        )
    season_team= db.get(SeasonTeam, player_season_team_data.season_team_id)
    if season_team is None:
        raise HTTPException(
            status_code=404,
            detail="Season team not found"
        )

    player_season_team = PlayerSeasonTeam(
        player_id=player_season_team_data.player_id,
        season_team_id=player_season_team_data.season_team_id,
        start_date=player_season_team_data.start_date,
        end_date=player_season_team_data.end_date
    )

    db.add(player_season_team)
    db.commit()
    db.refresh(player_season_team)

    return player_season_team

@router.put("/{player_season_team_id}", response_model=PlayerSeasonTeamResponse)
def update_player_season_team(
    player_season_team_id:int,
    player_season_team_data:PlayerSeasonTeamUpdate,
    db: Session = Depends(get_db)
):
    player_season_team = db.get(PlayerSeasonTeam, player_season_team_id)
    if player_season_team is None:
        raise HTTPException(
            status_code=404,
            detail="PlayerSeasonTeam not found"
        )
    update_data = player_season_team_data.model_dump(exclude_unset=True)
    
    new_start_date = update_data.get("start_date", player_season_team.start_date)
    new_end_date = update_data.get("end_date", player_season_team.end_date)

    if new_start_date is None:
        raise HTTPException(
            status_code=400,
            detail="StartDate cannot be null"
        )
    if new_end_date is not None and new_start_date >= new_end_date:
        raise HTTPException(
            status_code=400,
            detail="StartDate must be before end_date"
        )

    for field, value in update_data.items():
        setattr(player_season_team, field, value)

    db.commit()
    db.refresh(player_season_team)
    return player_season_team

@router.delete("/{player_season_team_id}", response_model=PlayerSeasonTeamResponse)
def delete_player_season_team(
    player_season_team_id:int,
    db:Session=Depends(get_db)
):
    player_season_team = db.get(PlayerSeasonTeam, player_season_team_id)
    if player_season_team is None:
        raise HTTPException(
            status_code=404,
            detail="PlayerSeasonTeam not found"
        )
    try:
        db.delete(player_season_team)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="PlayerSeasonTeam cannot be deleted because it is being used"
        )
    return player_season_team