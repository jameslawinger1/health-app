from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session 
from backend.database import SessionLocal 
from backend.services import meals as meal_service
from pydantic import BaseModel

router = APIRouter(prefix="/meals",tags=["Meals"])

class MealCreate(BaseModel):
    name: str
    ingredients: str
    calories: int
    protein: int
    fat: int
    carbs: int


def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally: 
        db.close()

@router.post("/")
def create_meal(meal: MealCreate, db: Session = Depends(get_db)):
    return meal_service.create_meal(
        db=db,
        name=meal.name,
        ingredients=meal.ingredients,
        calories=meal.calories,
        protein=meal.protein,
        fat=meal.fat,
        carbs=meal.carbs,
    )
@router.get("/")
def read_meals(db:Session = Depends(get_db)):
    return meal_service.get_meals(db)

