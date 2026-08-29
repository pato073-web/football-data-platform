from fastapi import FastAPI
from app.routers.countries import router as countries_router
from app.routers.competition import router as competitions_router

app = FastAPI(
    title = "Football Data Platform",
    description = "REST API for football competitions, teams, players and matches",
    version = "0.1.0",
)

app.include_router(countries_router)
app.include_router(competitions_router)

@app.get("/")
def root():
    return {"message": "Football Data Platform API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}