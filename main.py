from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .database import Base, engine
from .routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FitBuddy – AI Fitness Plan Generator",
    description="Generate personalized 7-day wellness plans with Gemini and store them in SQLite.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router)
