from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.player_season_team import PlayerSeasonTeam
from app.models.player import Player
from app.models.season_team import SeasonTeam
from app.schemas.player_season_team import PlayerSeasonTeamCreate, PlayerSeasonTeamResponse

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