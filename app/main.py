from fastapi import FastAPI

app = FastAPI(
    title = "Football Data Platform",
    description = "REST API for football competitions, teams, players and matches",
    version = "0.1.0",
)

@app.get("/")
def root():
    return {"message": "Football Data Platform API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}