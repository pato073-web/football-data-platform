from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.database import get_db
from app.models.country import Country
from app.schemas.country import CountryCreate, CountryResponse, CountryUpdate

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

@router.post("/", response_model=CountryResponse, status_code=201)
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
    
    return country

@router.put("/{country_id}", response_model=CountryResponse)
def update_country(
    country_id: int,
    country_data: CountryUpdate,
    db: Session = Depends(get_db)
):
    country = db.get(Country, country_id)
    if country is None:
        raise HTTPException(
            status_code=404,
            detail="Country not found"
        )
    update_data = country_data.model_dump(exclude_unset=True)

    if "name" in update_data and update_data["name"] is None:
        raise HTTPException(
            status_code=400,
            detail="name cannot be null"
        )
    if "code" in update_data and update_data["code"] is None:
        raise HTTPException(
            status_code=400,
            detail="Name cannot be null"
        )

    for field, value in update_data.items():
        setattr(country, field, value)

    try:
        db.commit()
        db.refresh(country)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code = 409,
            detail = "Country code already exists"
        )

    return country

@router.delete("/{country_id}", response_model=CountryResponse)
def delete_country(
    country_id:int,
    db: Session = Depends(get_db)
):
    country = db.get(Country, country_id)
    if country is None:
        raise HTTPException(
            status_code=404,
            detail="Country not found"
        )
    try:
        db.delete(country)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Country cannot be deleted because it is being used"
        )

    return country