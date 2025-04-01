from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session 
from backend.database import SessionLocal 
from backend.services import meals as meal_service

router = APIRouter(prefix="/meals",tags=["Meals"])


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()

@router.post("/")
def create_meal(name: str, ingredients: str, calories:int, protein:int,fat:int,carbs:int, db:Session = Depends(get_db)):
    return meal_service.create_meal(db,name,ingredients,calories,protein,fat,carbs)

@router.get("/")
def read_meals(db:Session = Depends(get_db)):
    return meal_service.get_meals(db)

