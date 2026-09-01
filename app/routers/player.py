from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.player import Player
from app.models.country import Country
from app.schemas.player import PlayerCreate, PlayerResponse, PlayerUpdate

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

@router.put("/{player_id}", response_model=PlayerResponse)
def update_player(
    player_id:int,
    player_data:PlayerUpdate,
    db: Session = Depends(get_db)
):
    player = db.get(Player, player_id)
    if player is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )
    update_data = player_data.model_dump(exclude_unset=True)

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

    if "birth_date" in update_data and update_data["birth_date"] is None:
        raise HTTPException(
            status_code=400,
            detail="BirthDate cannot be null"
        )
    
    for field, value in update_data.items():
        setattr(player, field, value)
        
    db.commit()
    db.refresh(player)
    return player

@router.delete("/{player_id}", response_model=PlayerResponse)
def delete_player(
    player_id:int,
    db:Session=Depends(get_db)
):
    player = db.get(Player, player_id)
    if player is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )
    try:
        db.delete(player)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Player cannot be deleted because it is being used"
        )
    return player