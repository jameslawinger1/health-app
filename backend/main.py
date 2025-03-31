from fastapi import FastAPI
from backend.database import Base, engine
from backend.models.meal import Meal
from backend.routers import meals

Base.metadata.create_all(bind=engine) 

app = FastAPI()
app.include_router(meals.router)
@app.get("/")
async def root():
    return {"message": "Welcome to the Health App!"}
