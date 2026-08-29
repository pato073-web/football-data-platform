from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.country import Country
from app.schemas.country import CountryCreate, CountryResponse

router = APIRouter(
    prefix="/countries",
    tags=["Countries"]
)

@router.get("/", response_model=list[CountryResponse])
def get_countries(db: Session = Depends(get_db)):
    statement = select(Country)
    countries = db.scalars(statement).all()

    return countries

@router.get("/{country_id}", response_model=CountryResponse)
def get_country(
    country_id: int,
    db: Session = Depends(get_db)
):
    country = db.get(Country, country_id)
    if country is None:
        raise HTTPException(
            status_code=404,
            detail=f"Country not found"
        )
    return country

@router.post("/", response_model=CountryResponse)
def create_country(
    country_data:CountryCreate,
    db: Session = Depends(get_db)
):
    country = Country(
        name = country_data.name,
        code = country_data.code
    )

    db.add(country)
    try:
        db.commit()
        db.refresh(country)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail = "Country code already exists"
        )
    db.commit()
    db.refresh(country)

    return country