from fastapi import FastAPI
from backend.database import Base, engine
from backend.models.meal import Meal
from fastapi import FastAPI
from backend.database import engine, Base
from backend.routers import meals  

# Create database tables
Base.metadata.create_all(bind=engine)

# Create the FastAPI app
app = FastAPI(title="Health App", version="0.1")

# Root route
@app.get("/")
async def root():
    return {"message": "Welcome to the Health App!"}

# Include feature routers
app.include_router(meals.router)
# app.include_router(workouts.router)
# app.include_router(habits.router)