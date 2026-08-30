from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.player import Player
from app.models.country import Country
from app.schemas.player import PlayerCreate, PlayerResponse

router = APIRouter(
    prefix="/players",
    tags=["Players"]
)

@router.get("/", response_model=list[PlayerResponse])
def get_players(db: Session = Depends(get_db)):
    statement = select(Player)
    players = db.scalars(statement).all()
    return players

@router.get("/{player_id}", response_model=PlayerResponse)
def get_player(
    player_id: int,
    db: Session = Depends(get_db)
):
    player = db.get(Player, player_id)
    if player is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )
    return player

@router.post("/", response_model=PlayerResponse, status_code=201)
def create_player(
    player_data: PlayerCreate,
    db: Session = Depends(get_db)
):
    country = db.get(Country, player_data.country_id)
    if country is None:
        raise HTTPException(
            status_code=404,
            detail = "Country not found"
        )
    player = Player(
        name=player_data.name,
        country_id=player_data.country_id,
        birth_date=player_data.birth_date,
    )

    db.add(player)
    db.commit()
    db.refresh(player)

    return player