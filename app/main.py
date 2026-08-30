from fastapi import FastAPI
from app.routers.countries import router as countries_router
from app.routers.competition import router as competitions_router
from app.routers.season import router as season_router
from app.routers.team import router as team_router
from app.routers.season_team import router as season_team_router

app = FastAPI(
    title = "Football Data Platform",
    description = "REST API for football competitions, teams, players and matches",
    version = "0.1.0",
)

app.include_router(countries_router)
app.include_router(competitions_router)
app.include_router(season_router)
app.include_router(team_router)
app.include_router(season_team_router)

@app.get("/")
def root():
    return {"message": "Football Data Platform API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}