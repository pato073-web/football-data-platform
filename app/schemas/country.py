from pydantic import BaseModel, ConfigDict


class CountryBase(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        from_attributes=True
    )

    name: str
    code: str


class CountryCreate(CountryBase):
    pass


class CountryResponse(CountryBase):
    id: int